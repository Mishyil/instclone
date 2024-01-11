from rest_framework.serializers import ModelSerializer
from notifications.models import Notification, UserNotification
from api.userprofile.serializers import UserProfileBaseinfoSerializers
from api.userpost.serializers import NotificationUserPostSerializer
from api.comment.serializers import NotificationCommentSerializer


class NotificationSerializer(ModelSerializer):
	"""
	Serializer class for displaying notifications.

	This serializer includes UserProfileBaseinfoSerializers for the user field, NotificationUserPostSerializer
	for the post field, and NotificationCommentSerializer for the comment field.

	"""

	user = UserProfileBaseinfoSerializers(read_only=True)
	post = NotificationUserPostSerializer(read_only=True)
	comment = NotificationCommentSerializer(read_only=True)
	
	class Meta:
		model = Notification
		fields = ['user', 'post', 'comment', 'notification_type', 'create_at']


class UserNotificationSerializer(ModelSerializer):
	"""
	Serializer class for displaying user notifications.

	This serializer includes NotificationSerializer for the notification field.

	"""

	notification = NotificationSerializer(read_only=True)

	class Meta:
		model = UserNotification
		fields = ['is_read', 'notification']


