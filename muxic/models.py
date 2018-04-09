import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

GENRE_CHOICE = (
    ('Rap_Hip Hop', 'Rap_Hip Hop'),
    ('R&B', 'R&B'),
    ('Ballad', 'Ballad'),
    ('EDM', 'EDM'),
    ('Country', 'Country'),
    ('etc', 'ETC'),
)


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    followers = models.IntegerField(default=0)
    followings = models.IntegerField(default=0)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    def __str__(self):
        return self.user.username


class Song(models.Model):
    # album = models.ForeignKey(Album, on_delete=models.CASCADE)
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    artist = models.CharField(max_length=500)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICE, default='EDM')
    logo = models.ImageField(upload_to='logosong', null=True)
    date_release = models.DateField(max_length=100, default=datetime.date.today)
    file = models.FileField(upload_to='filesong', null=True)
    lyric = models.TextField(max_length=10000, null=True)

    def get_absolute_url(self):
        return reverse('muxic:songdetail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.artist + ' - ' + self.title
