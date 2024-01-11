from django.urls import path
from .views import ProfileView, FollowersView, UserLogoutView

app_name = 'userprofile'

urlpatterns = [
	path('logout/', UserLogoutView.as_view(), name='logout'),
	path('followers/', FollowersView.as_view(), name='followers'),
	path('following/', FollowersView.as_view(), name='following'),
	path('', ProfileView.as_view(), name='userprofile'),
]	