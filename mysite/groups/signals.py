from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event, Group, UserGroup
from .utils import send_mail_async


@receiver(post_save, sender=Group)
def create_user_group(sender, instance, created, **kwargs):
    if created:
        UserGroup.objects.create(user=instance.owner, group=instance)


@receiver(post_save, sender=Event)
def new_event_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'Új esemény a csoportodban (%s): %s' % (
            instance.group.name, instance.title)
        message = '%s új eseményt vett fel (%s - %s).' % (
            instance.owner.username, instance.start, instance.end)
        recipient_list = [user.email for user in instance.group.users.all()]
        send_mail_async(subject, message, None, recipient_list)
