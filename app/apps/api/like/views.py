from django.shortcuts import get_object_or_404
from rest_framework import mixins, status
from userpost.models import UserPost
from .serializers import PostLikeSerializer
from like.models import PostLike
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response


class PostLikeAPIView(mixins.CreateModelMixin,
					mixins.DestroyModelMixin,
					mixins.ListModelMixin,
					mixins.RetrieveModelMixin,
					GenericViewSet):
	"""
	A viewset for handling Post Like operations.

	- create: Create a new like for a post.
	- destroy: Remove a like for a post.
	- list: List all likes for a post.
	- retrieve: Retrieve a specific like for a post.
	"""

	serializer_class = PostLikeSerializer

	def get_queryset(self):
		"""
		Get the queryset for the likes of a specific post.
		"""
		post_id = self.kwargs.get('post_pk')
		queryset = PostLike.objects.select_related('user').filter(post=post_id)
		return queryset

	def create(self, request, *args, **kwargs):
		"""
		Create a like for a post.

		"""
		post_id = self.kwargs.get('post_pk')
		user_id = request.user

		# Check if a record already exists for the given user and post
		existing_like = PostLike.objects.filter(user=user_id, post=post_id).first()
		if existing_like:
			return Response({'detail': 'You already liked this post.'},
				status=status.HTTP_400_BAD_REQUEST)


		# Get the post instance
		post = get_object_or_404(UserPost, id=post_id)

		# Initialize the serializer with user data and context
		serializer = PostLikeSerializer(data={'user': user_id},
								context={'request': request})

		# Validate the serializer data
		serializer.is_valid(raise_exception=True)

		# Save the like with the associated post
		serializer.save(post=post)

		return Response(serializer.data, status=status.HTTP_201_CREATED)
	