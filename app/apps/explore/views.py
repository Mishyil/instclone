from django.views.generic import ListView
from userpost.models import UserPost
from django.db.models import Count


class ExploreListView(ListView):
	"""
	View for displaying all posts sorted by the number of likes.

	"""

	model = UserPost
	context_object_name = 'posts'
	template_name = 'explore/explore.html'
	
	# Annotate the queryset with the count of likes and order it by the like count in descending order
	queryset = UserPost.objects.annotate(like_count=Count('likes')).order_by('-like_count')