from django.db import models
from django.contrib.auth.models import AbstractUser
from decouple import config
from django.urls import reverse
from storages.backends.s3boto3 import S3Boto3Storage
import uuid

class AvatarS3Storage(S3Boto3Storage):
	"""
	Class for storing avatar image files in Amazon S3 storage.

	"""
	# Define the location where avatar files will be stored in S3.
	location = 'avatar'

	def generate_unique_filename(self):
		"""
		Generate a unique file name using the uuid module.

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


class User(AbstractUser):
	"""
	Custom user model extending the AbstractUser.

	Attributes:
		bio (TextField): Text field for user biography, allowing up to 500 characters.
		avatar (ImageField): Image field for user avatar.
		follow (ManyToManyField): Many-to-many relationship for user following other users.
	"""

	bio = models.TextField(
		max_length=500, 
		blank=True)
	avatar = models.ImageField(
		storage=AvatarS3Storage(),
		blank=True)
	follow = models.ManyToManyField(
		'self', 
		related_name='following', 
		symmetrical=False, 
		blank=True)

	def get_url(self):
		"""
		Get the URL of the user's avatar.

		Returns:
			str: URL of the user's avatar.
		"""
		internal_url = self.avatar.url
		return internal_url.replace(config('AWS_S3_ENDPOINT_URL'),
									config('AWS_S3_ENDPOINT'))

	def get_absolute_url(self):
		"""
		Get the absolute URL of the user's profile.

		Returns:
			str: Absolute URL of the user's profile.
		"""
		return reverse('photo_detail', kwargs={'pk': self.pk})
