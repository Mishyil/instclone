from django.views.generic.detail import DetailView
from userpost.models import UserPost
from userpost.userpost_services import get_filtered_photos, extended_information

class PhotoView(DetailView):
	"""
	View for displaying details of a specific photo.

	"""

	model = UserPost
	template_name = 'userpost/photo_view.html'
	context_object_name = 'photo'

	def get_queryset(self):
		"""
		Get the queryset for the view, applying filters.

		Returns:
			QuerySet: Filtered queryset containing information about the specific photo.
		"""
		return get_filtered_photos(self)

	def get_context_data(self, **kwargs):
		"""
		Get the context data for the view, including extended information.

		Args:
			**kwargs: Additional keyword arguments.

		Returns:
			dict: Updated context data for rendering the template.
		"""
		context = super().get_context_data(**kwargs)
		return extended_information(self, context, **kwargs)
