from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from userprofile.models import User
from .serializers import UserProfileSerializer, UserListSerializator
from django.db.models import Count, Prefetch
from rest_framework import mixins
from api.userpost.permissions import ProfilePermission



class UserProfileRetriveAPIView(mixins.RetrieveModelMixin,
								mixins.UpdateModelMixin,
								GenericViewSet):
	"""
	View class for retrieving the profile information of a specific user.

	Uses UserProfileSerializer to serialize the user's profile information.
	Overrides get_object to customize the queryset and annotate additional 
	information such as follower count, following count, and post count.

	"""
	permission_classes = [ProfilePermission]
	serializer_class = UserProfileSerializer

	def get_object(self):
		username = self.kwargs.get('username')

		# Querying the user's profile and annotating follower count, following count, and post count.
		profile = User.objects.filter(username=username).annotate(
			follow_count=Count('following', distinct=True),
			following_count=Count('follow', distinct=True),
			post_count=Count('post', distinct=True)
		).only('username', 'avatar', 'bio').first()

		return profile


class UserFollowersListAPIView(ListAPIView):
	"""
	View class for retrieving the list of followers for a specific user.

	Uses UserListSerializator to serialize the list of followers.

	"""

	serializer_class = UserListSerializator

	def get_queryset(self):
		username = self.kwargs.get('username')

		# Querying users who follow the specified user.
		followers = User.objects.only('follow').filter(username=username)

		# Extracting usernames of followers.
		follower_usernames = followers.values_list('follow__username', flat=True)

		# Querying profiles of followers based on usernames.
		follower_profiles = User.objects.filter(
			username__in=follower_usernames).only('username', 'avatar')

		return follower_profiles


class UserFollowingListAPIView(ListAPIView):
	"""
	View class for retrieving the list of users whom a specific user is following.

	Uses UserListSerializator to serialize the list of users being followed.

	"""

	serializer_class = UserListSerializator

	def get_queryset(self):
		username = self.kwargs.get('username')

		# Querying users whom the specified user is following.
		following = User.objects.only('following').filter(username=username)

		# Extracting usernames of users being followed.
		following_usernames = following.values_list('following__username', flat=True)

		# Querying profiles of users being followed based on usernames.
		following_profiles = User.objects.filter(
			username__in=following_usernames).only('username', 'avatar')

		return following_profiles
