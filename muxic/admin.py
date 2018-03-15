from django.contrib import admin
from .models import *


# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['album_title', 'artist', 'album_date_release']
    list_filter = ['album_date_release']
    search_fields = ['album_title', 'artist']


admin.site.register(Album, AlbumAdmin)
admin.site.register(Song)
admin.site.register(UserProfile)