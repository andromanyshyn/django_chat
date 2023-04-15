from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed
from django.utils import timezone


class User(AbstractUser):
    pass


def participants_limit(sender, **kwargs):
    if kwargs['instance'].participants.count() > 2:
        raise ValidationError("You can't assign more than two participants")


class Thread(models.Model):
    """ Topic of Chat """
    participants = models.ManyToManyField(to=User, related_name='threads')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Thread id is {self.id}'


m2m_changed.connect(participants_limit, sender=Thread.participants.through)


class Message(models.Model):
    """ Messages in Topic """

    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField()
    thread = models.ForeignKey(to=Thread, on_delete=models.CASCADE, related_name='thread_messages')
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        thread = Thread.objects.get(id=self.thread.id)
        thread.update = timezone.now()
        thread.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Message id is {self.id} | sent by {self.sender}'
