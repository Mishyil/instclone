from rest_framework.generics import ListAPIView
from .serializers import ExploreSerializer
from userpost.models import UserPost
from django.db.models import Count
from .paginations import ExplorePagination


class ExploreAPIView(ListAPIView):
	"""
	API view for retrieving a list of posts sorted by the number of likes.

	"""

	serializer_class = ExploreSerializer
	pagination_class = ExplorePagination
	
	# Annotate the queryset with the count of unique users
	# who liked each post and order it by the like count in descending order
	queryset = UserPost.objects.annotate(
		like_count=Count('likes__user')
		).order_by('-like_count'
		).only('id', 'image')