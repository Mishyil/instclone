from django.urls import path
from .views import *

app_name = 'tools'

urlpatterns = [
	path('like/', post_like, name='post_like'),
	path('comment/', post_comment, name='post_comment'),
	path('follow/', follow_profile, name='follow_profile'),
	path('upload_photo/', upload_photo, name='upload_photo'),
	path('upload_avatar/', upload_avatar, name='upload_avatar'),
	path('delete_photo/', delete_photo, name='delete_photo')
]