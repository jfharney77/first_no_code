from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Chore


@receiver(pre_save, sender=Chore)
def stash_previous_assignee(sender, instance, **kwargs):
    """Before saving, stash the previous assigned_to so post_save can detect changes."""
    if instance.pk:
        try:
            old = Chore.objects.get(pk=instance.pk)
            instance._previous_assigned_to_id = old.assigned_to_id
        except Chore.DoesNotExist:
            instance._previous_assigned_to_id = None
    else:
        instance._previous_assigned_to_id = None


@receiver(post_save, sender=Chore)
def notify_assignee(sender, instance, created, **kwargs):
    """Send email when a chore is newly assigned or reassigned."""
    if not instance.assigned_to:
        return

    previous_id = getattr(instance, '_previous_assigned_to_id', None)

    if created or previous_id != instance.assigned_to_id:
        send_mail(
            subject=f'Chore assigned: {instance.title}',
            message=(
                f'Hi {instance.assigned_to.name},\n\n'
                f'You have been assigned a chore:\n\n'
                f'  Title: {instance.title}\n'
                f'  Date: {instance.date}\n'
                f'  Description: {instance.description or "(none)"}\n\n'
                f'Please check the office chore calendar for details.'
            ),
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[instance.assigned_to.email],
            fail_silently=True,
        )
