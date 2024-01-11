from django.db.models import Count, Prefetch
from userpost.models import UserPost
from comment.models import Comment
from like.models import PostLike

def get_filtered_photos(self):
	"""
	Retrieve information about a specific post, including user, comments, and likes count.

	Returns:
		QuerySet: QuerySet containing the filtered post information.
	"""
	# Get the photo_id from the URL parameters
	photo_id = self.kwargs.get('pk')

	# Prefetch related comments for optimization
	comments_prefetch = Prefetch('comments', queryset=Comment.objects.order_by(
		'-timestamp').select_related('user'))

	# Execute the main query with the prefetch
	photos = UserPost.objects.filter(pk=photo_id).select_related('user'
		).prefetch_related(comments_prefetch
		).annotate(likes_count=Count('likes'))

	return photos

def extended_information(self, context, **kwargs):
	"""
	Provide extended information to the context, including whether the current user
	has liked a specific photo.

	Returns:
		dict: Updated context dictionary.

	"""
	user = self.request.user
	# Get the liked photo IDs for the current user
	context['liked_photo_ids'] = PostLike.objects.filter(user=user).values_list('post_id', flat=True)

	return context
