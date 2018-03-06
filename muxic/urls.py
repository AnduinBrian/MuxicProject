from django.urls import path

from . import views
from muxic.views import *

app_name = 'muxic'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', UserFormView.as_view(), name='register'),
    path('add_album/', AddAlbumView.as_view(), name='add_album'),
    path('user/', UserView.as_view(), name='user'),
]
