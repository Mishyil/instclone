from django.db import models
from django.conf import settings
from comment.models import Comment
from userpost.models import UserPost


class PostLike(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	post = models.ForeignKey(UserPost, related_name='likes', on_delete=models.CASCADE)

	class Meta:
		unique_together = ('user', 'post')


class CommentLike(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE)


