import redis
from django.conf import settings
from celery import shared_task
from comment.models import Comment
from userpost.models import UserPost
from userprofile.models import User
from .models import Notification, UserNotification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Initialize the Redis client for communication
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=3)

@shared_task
def create_notification(from_profile, notification_type, to_profile=None, post=None, comment=None):
	"""
	Function to create and distribute notifications to specific users.
	If the event is occurring for the first time (i.e., the record is created),
	notifications are generated for specific users, and WebSocket notifications are sent.

	Args:
		from_profile (int): ID of the user initiating the action.
		notification_type (int): Type of the notification.
			LIKE = 1
			FOLLOW = 2
			COMMENT = 3
			NEW_POST = 4
		to_profile (int): ID of the target user for the notification (optional).
		post (int): ID of the post related to the notification (optional).
		comment (int): ID of the comment related to the notification (optional).
	"""

	# Get the user initiating the action
	from_user = User.objects.get(id=from_profile)

	# Get the post related to the notification (if available)
	if post is not None:
		post = UserPost.objects.get(id=post)

	# Get the comment related to the notification (if available)
	if comment is not None:
		comment = Comment.objects.get(id=comment)

	# Attempt to get or create the notification record
	notification, create = Notification.objects.get_or_create(
		notification_type=notification_type,
		user=from_user,
		post=post,
		comment=comment
	)

	if create:
		# If this is the first occurrence of the event (i.e., the record is created)

		if notification_type == 4:
			# If the notification type is 4 (creation of a new post),
			# notify all followers of the user initiating the action

			# Get all followers of the user
			followers = from_user.following.all()

			# Create user notifications for each follower
			user_notifications = [
				UserNotification(user=follower, notification=notification)
				for follower in followers
			]

			# Bulk create user notifications
			UserNotification.objects.bulk_create(user_notifications)

			# Get the IDs of the followers
			followers_ids = [follower.id for follower in followers]

			# Get the channel names for followers
			channel_names = redis_client.mget([f'user_{id}_channel' for id in followers_ids])

		else:
			# If the notification type is not 4 (other types of notifications)

			# Get the target user for the notification
			to_user = User.objects.get(id=to_profile)

			# Check if the target user is not the same as the user initiating the action
			if to_user != from_user:
				# Create a user notification for the target user
				UserNotification.objects.create(
					user=to_user,
					notification=notification
				)

			# Get the channel name for the target user
			channel_names = [redis_client.get(f"user_{to_profile}_channel")]

		# Send WebSocket notifications to the specified channels
		for channel_name in channel_names:
			if channel_name:
				channel_layer = get_channel_layer()
				async_to_sync(channel_layer.send)(
					channel_name.decode('utf-8'),
					{
						"type": "new_notification"
					}
				)
