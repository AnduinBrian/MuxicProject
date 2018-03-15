import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    followers = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    following = models.DecimalField(max_digits=10, decimal_places=1, default=0)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Album(models.Model):
    album_title = models.CharField(max_length=1000)
    artist = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.CharField(max_length=1000, )
    album_date_release = models.DateField(max_length=100, default=datetime.date.today)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=1000)
    artist = models.CharField(max_length=500)
    song_logo = models.CharField(max_length=1000)
    song_date_release = models.DateField(max_length=100, default=datetime.date.today)

    def __str__(self):
        return self.artist + ' - ' + self.song_title
