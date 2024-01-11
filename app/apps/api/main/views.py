from rest_framework.generics import CreateAPIView
from userprofile.models import User
from .serializers import RegisterUserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserRegisterAPIView(CreateAPIView):
	"""
	API view for user registration.

	This view allows users to register by handling the creation of new user accounts.
	It uses the RegisterUserSerializer for validating and processing user registration data.

	"""

	queryset = User.objects.all()
	serializer_class = RegisterUserSerializer

	def perform_create(self, serializer):
		"""
		Additional actions after successful user creation.

		"""
		user = serializer.save()
		login(self.request, user)


class UserLogInAPIView(APIView):
	"""
	API view for user login.

	This view handles user login by authenticating provided credentials.

	"""

	def post(self, request, *args, **kwargs):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return Response({'detail':'LogIn True'})
		else:
			return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401)


class UserLogOutAPIView(APIView):
	"""
	API view for user logout.

	This view handles user logout by terminating the user's session.

	"""

	def get(self, request, *args, **kwargs):
		logout(request)
		return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
