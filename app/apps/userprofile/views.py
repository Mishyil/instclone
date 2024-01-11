from django.shortcuts import render
from django.views.generic import ListView
from .models import User
from .userprofile_services import extended_information, get_filtered_photos, get_filtered_profiles
from django.contrib.auth.views import LogoutView

class ProfileView(ListView):
	"""
	View for displaying user profile and associated photos.

	"""

	context_object_name = 'photos'
	template_name = 'userprofile/profile.html'

	def get_queryset(self):
		"""
		Get the queryset of photos for the current user.

		Returns:
			QuerySet: Filtered queryset containing photos for the current user.
		"""
		return get_filtered_photos(self)
	
	def get_context_data(self, **kwargs):
		"""
		Get additional context data for the profile view.

		Returns:
			dict: Updated context data with extended information.
		"""
		context = super().get_context_data(**kwargs)
		return extended_information(self, context, **kwargs)

class FollowersView(ListView):
	"""
	View for displaying followers of a user.

	"""

	model = User
	template_name = 'userprofile/followers_view.html'
	context_object_name = 'followers'

	def get_queryset(self):
		"""
		Get the queryset of followers for the current user.

		Returns:
			QuerySet: Filtered queryset containing followers for the current user.
		"""
		return get_filtered_profiles(self)

class UserLogoutView(LogoutView):
	"""
	View for logging out a user.

	"""
	
	next_page = '/'