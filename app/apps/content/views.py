from django.shortcuts import render
from django.views.generic import ListView
from .content_services import extended_information, get_filtered_photos


class ContentView(ListView):
	"""
	Class for displaying the feed of posts for the current user.
	
	"""
	context_object_name = 'photos'
	template_name = 'content/content.html'

	def get_queryset(self):
		# Retrieve and return the queryset for the posts
		return get_filtered_photos(self)
	
	def get_context_data(self, **kwargs):
		# Get additional information and add it to the context
		context = super().get_context_data(**kwargs)
		return extended_information(self, context, **kwargs)


