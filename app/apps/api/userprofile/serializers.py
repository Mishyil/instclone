from rest_framework.serializers import ModelSerializer
from userprofile.models import User
from rest_framework import serializers


class UserNameSerializer(ModelSerializer):
	"""
	Serializer class for displaying only the username of a User model.

	"""

	class Meta:
		model = User
		fields = ['username']


class UserProfileBaseinfoSerializers(ModelSerializer):
	"""
	Serializer class for displaying the id, username, and avatar of a User model.

	"""

	class Meta:
		model = User
		fields = ['id', 'username', 'avatar']


class UserProfileSerializer(ModelSerializer):
	"""
	Serializer class for displaying detailed user profile information.

	This serializer includes the username, avatar, bio, follow count, following count, and post count.

	"""

	follow_count = serializers.IntegerField(read_only=True)
	following_count = serializers.IntegerField(read_only=True)
	post_count = serializers.IntegerField(read_only=True)

	class Meta:
		model = User
		fields = ['username', 'avatar', 'bio', 'follow_count', 'following_count', 'post_count']


class UserListSerializator(ModelSerializer):
	"""
	Serializer class for displaying a list of users, including only the username and avatar.

	"""

	class Meta:
		model = User
		fields = ['username', 'avatar']
