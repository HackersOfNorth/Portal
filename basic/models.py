from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=10)
    friends = models.ManyToManyField('UserProfile', through='Friendship', through_fields=('person', 'friend'))
    pending_messages = models.ManyToManyField('PendingMessage', through='MessagePool', through_fields=('person', 'message'))

    def __unicode__(self):
        return self.user.username


class Friendship(models.Model):
    person = models.ForeignKey('UserProfile')
    friend = models.ForeignKey('UserProfile', related_name='friend')

    def __unicode__(self):
        return str(self.person) + '->' + str(self.friend)


class PendingMessage(models.Model):
    message = models.CharField(max_length=100)
    source = models.ForeignKey('UserProfile')
    message_type = models.CharField(max_length=100)

    def __unicode__(self):
        return self.message


class MessagePool(models.Model):
    person = models.ForeignKey('UserProfile')
    message = models.ForeignKey('PendingMessage')

