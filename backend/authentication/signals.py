import logging

from allauth.account.models import EmailAddress
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger('sasta')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_admin_email(sender, instance, created, **kwargs):
    ''' Ensure emailaddress is automatically verified for superuser accounts'''
    if not (created and instance.is_superuser and instance.email):
        return
    try:
        EmailAddress.objects.update_or_create(
            user=instance,
            email=instance.email,
            defaults={'verified': True, 'primary': True},
        )
        logger.info(f'Automatically verified email {instance.email} for {instance}')
    except Exception:
        logger.exception('Failed to automatically verify admin email')
