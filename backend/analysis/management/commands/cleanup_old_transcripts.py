from datetime import date
from dateutil.relativedelta import relativedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from analysis.models import Transcript


class Command(BaseCommand):
    help = 'List (and optionally delete) transcripts older than N months.'

    def add_arguments(self, parser):
        parser.add_argument(
            'months',
            type=int,
            help='Count transcripts added more than this many months ago.',
        )
        parser.add_argument(
            '--remove',
            action='store_true',
            default=False,
            help='Delete the matching transcripts and their analysis runs.',
        )

    def handle(self, *args, **options):
        months = options['months']
        if months < 1:
            raise CommandError('months must be a positive integer.')

        cutoff = date.today() - relativedelta(months=months)
        old_transcripts = Transcript.objects.filter(
            date_added__lt=cutoff
        ).select_related('corpus__user')

        total = old_transcripts.count()
        if total == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'No transcripts older than {months} month(s) found.'
                )
            )
            return

        # Group by user
        user_counts: dict[User, list[Transcript]] = {}
        for transcript in old_transcripts:
            user = transcript.corpus.user
            user_counts.setdefault(user, []).append(transcript)

        self.stdout.write(
            f'Transcripts older than {months} month(s) (before {cutoff}):\n'
        )
        for user, transcripts in sorted(
            user_counts.items(), key=lambda item: item[0].username
        ):
            self.stdout.write(f'  {user.username}: {len(transcripts)} transcript(s)')

        self.stdout.write(f'\nTotal: {total} transcript(s)')

        if options['remove']:
            # AnalysisRun has on_delete=CASCADE so they are removed automatically.
            deleted_count, _ = old_transcripts.delete()
            self.stdout.write(
                self.style.WARNING(
                    f'Deleted {total} transcript(s) and their related objects '
                    f'({deleted_count} total rows removed).'
                )
            )
        else:
            self.stdout.write(
                self.style.NOTICE(
                    'Run with --remove to delete these transcripts and their analysis runs.'
                )
            )
