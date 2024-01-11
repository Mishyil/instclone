from django.db.models import Count
from userpost.models import UserPost
from userprofile.models import User

def get_filtered_photos(self):
	"""
	Retrieve filtered photos for a specific user.

	Returns:
		QuerySet: Filtered queryset containing photos for the specified user.
	"""
	current_user = self.kwargs.get('username')
	photos = UserPost.objects.filter(user__username=current_user)
	return photos

def extended_information(self, context, **kwargs):
	"""
	Provide extended information for the user profile.

	Args:
		context (dict): The current context data.
		**kwargs: Additional keyword arguments.

	Returns:
		dict: Updated context data with extended information.
	"""
	user = self.request.user
	current_page = self.kwargs.get('username')
	current_user = User.objects.filter(username=current_page
						).annotate(
							follow_count=Count('following', distinct=True),
							following_count=Count('follow', distinct=True)
						).first()
	context['profile'] = current_user
	context['post_count'] = self.object_list.count()
	context['profile_owner'] = user.username == current_page
	context['is_following'] = self.request.user.follow.filter(id=current_user.id).exists()
	return context

def get_filtered_profiles(self):
	"""
	Get filtered profiles based on the current view type (followers or following).

	Returns:
		QuerySet: Filtered queryset containing followers or following profiles.
	"""
	username = self.kwargs.get('username')
	user = User.objects.get(username=username)
	if 'followers' in self.request.path:
		followers = user.following.all()
	elif 'following' in self.request.path:
		followers = user.follow.all()
	return followers
