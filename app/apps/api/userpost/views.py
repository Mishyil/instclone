from django.db.models import Count
from rest_framework.response import Response
from like.models import PostLike
from userpost.models import UserPost
from .serializers import UserPostSerializer, ProfileUserPostsSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from notifications.tasks import create_notification
from django.db.models import OuterRef, Exists
from .pagination import ProfilePostPagination


class UserPostAPIView(mixins.CreateModelMixin,
					  mixins.RetrieveModelMixin,
					  mixins.UpdateModelMixin,
					  mixins.DestroyModelMixin,
					  GenericViewSet):
	
	"""
	View class for displaying and managing individual UserPost objects.

	Inherits from GenericViewSet and utilizes mixins to implement
	basic CRUD operations (Create, Retrieve, Update, Delete) for the UserPost model.

	Attributes:
	- queryset: Database query for selecting UserPost objects. Here, select_related is used for prefetching related
			user data, only for selecting specific fields, annotate Count for counting likes, and annotate for
			adding a computed field likes_count to each object.
	"""
	serializer_class = UserPostSerializer

	def get_object(self):
		# Get the 'pk' (primary key) from the URL kwargs
		pk = self.kwargs.get('pk')

		# Define a subquery to check if the current user has liked the post
		likes_subquery = PostLike.objects.filter(post=OuterRef('pk'), user=self.request.user)

		# Query the UserPost model, annotate with likes_count and current_user_liked, and retrieve the necessary fields
		queryset = UserPost.objects.select_related('user').annotate(
			likes_count=Count('likes'),
			current_user_liked=Exists(likes_subquery),
		).filter(pk=pk).only(
			'user__username', 
			'user__avatar',
			'user__id',
			'image',
			'caption',
			'timestamp'
		).first()

		return queryset


class ProfileUserPosts(mixins.CreateModelMixin,
					   mixins.ListModelMixin,
					   GenericViewSet):
	"""
	View class for displaying UserPost objects related to a specific user profile.

	Utilizes ListAPIView for displaying a list of UserPost objects in a user's profile.

	"""
	serializer_class = ProfileUserPostsSerializer
	pagination_class = ProfilePostPagination

	def get_queryset(self):
		# Get the username from URL kwargs
		username = self.kwargs.get('username')

		# Filter UserPost objects related to the specified user's profile, selecting only the 'image' field
		queryset = UserPost.objects.filter(user__username=username).only('image').all()
		
		return queryset
	
	async def create(self, request, *args, **kwargs):

		# Create a serializer and validate the data
		serializers = UserPostSerializer(data=request.data, context={'request': request})
		serializers.is_valid(raise_exception=True)

		# Save the object to the database
		serializers.save()

		# Get the post_id and profile_id from the created instance's data
		post_id = serializers.data.get('id')
		profile_id = serializers.data.get('profile', {}).get('id')

		# Use a celery task to asynchronously create a notification
		create_notification.delay(
			from_profile=profile_id,
			notification_type=4,
			post=post_id
		)

		return Response(serializers.data)