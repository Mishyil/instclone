from django.db import models
from django.conf import settings
from django.utils import timezone
from decouple import config
from storages.backends.s3boto3 import S3Boto3Storage
import uuid
from django.contrib.auth.models import User


class PhotoS3Storage(S3Boto3Storage):
	"""
	Class for storing image files of user posts in Amazon S3 storage.

	"""

	# Define the location where files will be stored in S3.
	location = 'photos'

	def generate_unique_filename(self):
		"""
		Generate a unique file name using the uuid module.

		Returns:
			str: Unique file name.
		"""
		return f'{uuid.uuid4()}.jpg'

	def save(self, name, content, max_length=None, **kwargs):
		"""
		Override the save method to generate a unique file name before saving.

		Returns:
			str: File name after saving.
		"""

		# Generate a unique file name.
		name = self.generate_unique_filename()

		# Call the parent save method with the unique file name.
		return super().save(name, content, max_length, **kwargs)



class UserPost(models.Model):
	"""
	Model representing a user's post.

	Attributes:
		user (ForeignKey): Reference to the user who created the post.
		image (ImageField): Image file representing the content of the post.
		caption (TextField): Optional text caption for the post.
		timestamp (DateTimeField): Timestamp indicating when the post was created.
	"""

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='post')
	image = models.ImageField(
		storage=PhotoS3Storage())
	caption = models.TextField(
		blank=True)
	timestamp = models.DateTimeField(
		default=timezone.now)

	class Meta:
		ordering = ['-timestamp']

	def number_of_likes(self):
		"""
		Get the number of likes for the post.

		Returns:
			int: Number of likes for the post.
		"""
		return self.likes.count()

	def get_avatar_url(self):
		"""
		Get the avatar URL of the user who created the post.

		Returns:
			str: Avatar URL of the user.
		"""
		return self.user.avatar.url.replace(config('AWS_S3_ENDPOINT_URL'), 
											config('AWS_S3_ENDPOINT'))

	def get_url(self):
		"""
		Get the internal URL of the post's image.

		Returns:
			str: Internal URL of the post's image.
		"""
		internal_url = self.image.url
		return internal_url.replace(config('AWS_S3_ENDPOINT_URL'),
									config('AWS_S3_ENDPOINT'))

	def delete(self, *args, **kwargs):
		"""
		Override the delete method to delete associated image before deleting the post.

		Args:
			*args: Additional positional arguments.
			**kwargs: Additional keyword arguments.
		"""
		self.image.delete(save=False)
		super().delete(*args, **kwargs)
