from typing import Dict, Optional, Sequence, Tuple, Type

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Model

from analysis.models import (AnalysisRun, AssessmentMethod, CompoundFile,
                             Transcript, UploadFile)

# Number of changed paths to print per model when not running with --execute.
PREVIEW_LIMIT = 10

# Models to scan, paired with the FileField names and any plain text field
# names (e.g. Transcript.extracted_filename) that may hold a path prefixed
# with the old media root.
TARGETS: Tuple[Tuple[Type[Model], Sequence[str], Sequence[str]], ...] = (
    (Transcript, ('content', 'parsed_content', 'corrected_content'), ('extracted_filename',)),
    (UploadFile, ('content',), ()),
    (AssessmentMethod, ('content',), ()),
    (AnalysisRun, ('query_file', 'annotation_file', 'form_file', 'annotated_chat_file'), ()),
    (CompoundFile, ('content',), ()),
)


class Command(BaseCommand):
    help = (
        'Fix stale absolute file paths after the media root has moved. Scans '
        'Transcript, UploadFile, AssessmentMethod, AnalysisRun, and CompoundFile '
        'records for any stored path containing `--old-media-root` and replaces '
        'that prefix with `--new-media-root`. Runs as a dry run unless --execute '
        'is given.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--old-media-root',
            required=True,
            type=str,
            help='Absolute media root currently stored in file paths, to be replaced.',
        )
        parser.add_argument(
            '--new-media-root',
            required=True,
            type=str,
            help='Absolute media root to replace `--old-media-root` with.',
        )
        parser.add_argument(
            '--execute',
            action='store_true',
            default=False,
            help=(
                'Apply the changes to the database. Without this flag the command '
                'runs as a dry run: it only prints the old and new paths for the '
                f'first {PREVIEW_LIMIT} affected files of each model, and no data '
                'is written.'
            ),
        )

    def handle(self, *args, **options):
        old_root = options['old_media_root'].rstrip('/')
        new_root = options['new_media_root'].rstrip('/')
        execute = options['execute']

        if not old_root or not new_root:
            raise CommandError(
                '--old-media-root and --new-media-root must both be non-empty.')
        if old_root == new_root:
            raise CommandError(
                '--old-media-root and --new-media-root must be different.')

        total_found = 0
        total_updated = 0
        for model, file_fields, char_fields in TARGETS:
            found, updated = self._migrate_model(
                model, file_fields, char_fields, old_root, new_root, execute)
            total_found += found
            total_updated += updated

        self.stdout.write('')
        if execute:
            self.stdout.write(self.style.SUCCESS(
                f'Done: updated {total_found} path(s) across {total_updated} record(s).'))
        else:
            self.stdout.write(self.style.NOTICE(
                f'Dry run: {total_found} path(s) across {total_updated} record(s) would be '
                'updated. Re-run with --execute to apply these changes.'))

    def _migrate_model(self, model: Type[Model], file_fields: Sequence[str],
                       char_fields: Sequence[str], old_root: str, new_root: str,
                       execute: bool) -> Tuple[int, int]:
        '''Scan every instance of `model` for `old_root` inside `file_fields`
        (FileFields, matched on their stored name) and `char_fields` (plain
        text fields). Prints a preview, or applies the replacement when
        `execute` is True. Returns (paths found, records affected).'''
        self.stdout.write(f'{model.__name__}:')
        found = 0
        updated = 0
        previewed = 0

        for instance in model.objects.all().iterator():
            changes: Dict[str, str] = {}

            for field_name in (*file_fields, *char_fields):
                old_value = self._field_value(instance, field_name)
                new_value = self._replace_root(old_value, old_root, new_root)
                if new_value is None:
                    continue
                found += 1
                changes[field_name] = new_value
                if not execute and previewed < PREVIEW_LIMIT:
                    self.stdout.write(f'  [{field_name}] {old_value} -> {new_value}')
                    previewed += 1

            if changes:
                updated += 1
                if execute:
                    # Go through the queryset, not instance.save(), to avoid
                    # triggering post_save signals (TAM re-parsing, Compound
                    # table rebuilding, ...) that are unrelated to this path fix.
                    model.objects.filter(pk=instance.pk).update(**changes)

        self._report(found, updated, execute)
        return found, updated

    def _report(self, found: int, updated: int, execute: bool) -> None:
        '''Print the per-model summary line(s) for `_migrate_model`.'''
        if found == 0:
            self.stdout.write('  No matching paths found.')
            return
        verb = 'Updated' if execute else 'Found'
        self.stdout.write(f'  {verb} {found} path(s) across {updated} record(s).')
        if not execute and found > PREVIEW_LIMIT:
            self.stdout.write(f'  ... and {found - PREVIEW_LIMIT} more not shown.')

    @staticmethod
    def _field_value(instance: Model, field_name: str) -> Optional[str]:
        '''Return the current stored path for `field_name`, whether it is a
        FileField (read via its `.name`) or a plain text field.'''
        value = getattr(instance, field_name)
        return value.name if hasattr(value, 'name') else value

    @staticmethod
    def _replace_root(value: Optional[str], old_root: str, new_root: str) -> Optional[str]:
        '''Return `value` with `old_root` replaced by `new_root`, or None if
        `value` is empty or does not contain `old_root`.'''
        if not value or old_root not in value:
            return None
        return value.replace(old_root, new_root)
