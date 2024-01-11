from rest_framework.generics import ListAPIView
from comment.models import Comment
from .serializers import ContentModelSerializer
from .paginations import StandardResultsSetPagination
from userpost.models import UserPost
from django.db.models import Prefetch, OuterRef, Exists, Count
from like.models import PostLike


class ContentListAPIView(ListAPIView):
	"""
	API view for listing content in the feed.

	"""

	serializer_class = ContentModelSerializer
	pagination_class = StandardResultsSetPagination

	def get_queryset(self):
		"""
		Get the queryset of content with related user data, comments, and like counts.

		"""
		user = self.request.user
		likes_subquery = PostLike.objects.filter(post=OuterRef('pk'), user=user)

		return UserPost.objects.select_related('user').only('user__username', 'user__avatar', 'image', 'caption', 'timestamp').prefetch_related(
			Prefetch('comments', queryset=Comment.objects.select_related('user').only('user__username', 'post', 'text'))
		).annotate(
			current_user_liked=Exists(likes_subquery),
			likes_count=Count('likes')
		)