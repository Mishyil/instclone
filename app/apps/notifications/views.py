from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import UserNotification
from .notifications_services import filtered_notifications

@login_required
def get_unread_notifications_count(request):
	"""
	Get the count of unread notifications for the authenticated user.

	Returns:
		JsonResponse: JSON response containing the unread notifications count.
	"""
	count = UserNotification.objects.filter(user=request.user, is_read=False).count()
	return JsonResponse({'unread_count': count})

@login_required
@require_POST
def mark_notifications_read(request):
	"""
	Mark all notifications for the authenticated user as read.

	Returns:
		JsonResponse: JSON response indicating the success of marking notifications as read.
	"""
	request.user.notifications.filter(is_read=False).update(is_read=True)
	return JsonResponse({'success': True, 'unread_count': 0})

class NotificationsView(ListView):
	"""
	View for displaying notifications for the current authenticated user.

	"""

	template_name = 'notifications/notifications.html'
	context_object_name = 'notifications'

	def get_queryset(self):
		"""
		Get the queryset of notifications for the authenticated user.

		Returns:
			QuerySet: Notifications queryset.
		"""
		return filtered_notifications(self)
