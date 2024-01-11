from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from userpost.models import UserPost
from api.userprofile.serializers import UserProfileBaseinfoSerializers
from rest_framework import serializers


class UserPostSerializer(ModelSerializer):

	"""
	Serializer class for displaying information about a specific UserPost.

	"""
	profile = UserProfileBaseinfoSerializers(read_only=True, source='user')
	likes_count = serializers.IntegerField(read_only=True)
	current_user_liked = serializers.BooleanField(read_only=True)
	create_date = serializers.DateTimeField(read_only=True, source='timestamp')
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())
	timestamp = serializers.HiddenField(default=timezone.now)

	class Meta:
		model = UserPost
		fields = '__all__'


	def save(self, **kwargs):
		return super().save(**kwargs)

class ProfileUserPostsSerializer(ModelSerializer):
	"""
	Serializer class for displaying photos in UserProfile.

	"""
	class Meta:
		model = UserPost
		fields = ['image']


class NotificationUserPostSerializer(ModelSerializer):
	"""
	Serializer class for dispaying photo in Notification bar.
	
	"""


	class Meta:
		model = UserPost
		fields = ['id', 'image']