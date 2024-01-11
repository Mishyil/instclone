from django.shortcuts import get_object_or_404
from comment.models import Comment
from userpost.models import UserPost
from .serializers import CommentSerializers
from .pagination import CommentdResultsSetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from notifications.tasks import create_notification
from rest_framework import status




class CommentListAPIView(ModelViewSet):

	"""
	A ViewSet for handling comments related to a specific post.

	This ViewSet provides CRUD operations for comments, where each comment is associated with a particular post.
	It also includes a custom create method to handle comment creation and trigger notifications.

	"""

	serializer_class = CommentSerializers
	pagination_class = CommentdResultsSetPagination

	def get_queryset(self):
		# Get the post identifier from the URL path
		post_id = self.kwargs.get('post_pk')

		# Filter comments related to the specified post
		queryset = Comment.objects.filter(post=post_id).select_related('user').all()
		return queryset

	async def create(self, request, *args, **kwargs):
		# Get the post identifier from the URL path
		post_id = kwargs.get('post_pk')

		# Get the post by identifier or return 404 if the post is not found
		post = get_object_or_404(UserPost, id=post_id)
		
		# Initialize the serializer with data from the request
		serializer = CommentSerializers(data=request.data)

		# Check the validity of the data, raising an exception in case of an error
		serializer.is_valid(raise_exception=True)

		# Save the comment with the current user and post
		serializer.save(user=request.user, post=post)

		# Get identifiers for the notification
		from_profile = serializer.instance.user.id
		to_profile = post.user.id
		post_id = post.id
		comment_id = serializer.instance.id

		# Trigger a task to create the notification
		create_notification.delay(
			from_profile=from_profile,
			to_profile=to_profile,
			notification_type=3,
			post=post_id,
			comment=comment_id
		)

		# Return a response with the data of the created comment and a status of 201 Created
		return Response(serializer.data, status=status.HTTP_201_CREATED)