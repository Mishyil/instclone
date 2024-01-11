from django.db import models
from django.conf import settings
from comment.models import Comment
from userpost.models import UserPost


# Constants representing notification types
LIKE = 1
FOLLOW = 2
COMMENT = 3
NEW_POST = 4

# Choices for the notification type field
NOTIFICATION_TYPE = (
	(LIKE, 'Like'),
	(FOLLOW, 'Follow'),
	(COMMENT, 'Comment'),
	(NEW_POST, 'New_post'),
)

class Notification(models.Model):
	"""
	Model for storing information about a specific notification
	
	"""
	# Type of the notification (e.g., Like, Follow, Comment, New_post)
	notification_type = models.PositiveBigIntegerField(
		choices=NOTIFICATION_TYPE)

	# Timestamp indicating when the notification was created
	create_at = models.DateTimeField(
		auto_now_add=True)

	# User associated with the notification
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name='event',
		on_delete=models.CASCADE)

	# Post associated with the notification (optional)
	post = models.ForeignKey(
		UserPost,
		on_delete=models.CASCADE,
		null=True,
		blank=True)

	# Comment associated with the notification (optional)
	comment = models.ForeignKey(
		Comment,
		on_delete=models.CASCADE,
		null=True,
		blank=True)
	
	class Meta:
		# Order notifications by creation timestamp in descending order
		ordering = ['-create_at']

class UserNotification(models.Model):
	"""
	Model for storing information about a specific user's notification status
	
	"""
	# User associated with the notification
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name='notifications',
		on_delete=models.CASCADE)

	# Notification associated with the user
	notification = models.ForeignKey(
		Notification,
		on_delete=models.CASCADE)

	# Flag indicating whether the user has read the notification
	is_read = models.BooleanField(
		default=False)


