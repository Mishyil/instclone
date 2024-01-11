from rest_framework.serializers import ModelSerializer
from comment.models import Comment
from api.userprofile.serializers import UserProfileBaseinfoSerializers, UserNameSerializer
from rest_framework import serializers
from django.utils import timezone



class CommentContentSerializers(ModelSerializer):
	"""
	Serializer for displaying comments in the feed of posts.
	
	"""
	username = UserNameSerializer(read_only=True, source='user')

	class Meta:
		model = Comment
		fields = ['username', 'text']


class CommentSerializers(ModelSerializer):
	"""
	Serializer for displaying comments for a specific post.

	"""
	user_comment = UserProfileBaseinfoSerializers(read_only=True, source='user')
	create_time = serializers.DateTimeField(read_only=True, source='timestamp')
	timestamp = serializers.HiddenField(default=timezone.now)

	class Meta:
		model = Comment
		fields = ['id', 'user_comment', 'text', 'timestamp', 'create_time']


class NotificationCommentSerializer(ModelSerializer):
	"""
	Serializer for displaying comments in notifications.
	
	"""

	class Meta:
		model = Comment
		fields = ['text']

