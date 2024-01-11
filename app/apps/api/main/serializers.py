from rest_framework.serializers import ModelSerializer
from userprofile.models import User


class RegisterUserSerializer(ModelSerializer):
	"""
	Serializer class for user registration.

	This serializer is used for handling user registration by defining the fields
	and their properties. The password field is marked as write-only to ensure
	it is not included in responses.
	
	"""

	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'password']
		extra_kwargs = {'password': {'write_only': True}} 

	def create(self, validated_data):
		"""
		Create method for handling user creation during registration.

		"""
		user = User(
			username=validated_data['username'],
			email=validated_data['email']
		)
		user.set_password(validated_data['password'])
		user.save()
		return user
