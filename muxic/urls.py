from django.urls import path

from . import views
from muxic.views import *

app_name = 'muxic'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('add_album/', AddAlbumView.as_view(), name='add_album'),
    path('user/<str:username>', ProfileView.as_view(), name='user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
