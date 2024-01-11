from django.db import models
from django.utils import timezone
from django.conf import settings
from userpost.models import UserPost


class Comment(models.Model):
	# Represents a comment made by a user on a post.

	# User who made the comment
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
							 on_delete=models.CASCADE)
	
	# Post to which the comment is associated
	post = models.ForeignKey(UserPost,
							 related_name='comments',
							 on_delete=models.CASCADE)
	
	# Text content of the comment
	text = models.TextField()
	
	# Timestamp indicating when the comment was created
	timestamp = models.DateTimeField(default=timezone.now)

