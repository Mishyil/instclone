from rest_framework.generics import ListAPIView
from django.db.models import Prefetch
from notifications.models import Notification, UserNotification
from .serializers import UserNotificationSerializer
from .pagitation import NotificationPaginator


class NotificationListAPIView(ListAPIView):
	"""
	View class for displaying a list of notifications for a current user.

	This view includes pagination using NotificationPaginator and uses UserNotificationSerializer
	for displaying the notifications.

	"""

	pagination_class = NotificationPaginator
	serializer_class = UserNotificationSerializer

	def get_queryset(self):
		username = self.kwargs.get('username')

		# Query for notifications, selecting related user, post, and comment fields
		notification_query = Notification.objects.order_by('create_at'
		).select_related('user', 'post', 'comment'
		).only('notification_type', 'create_at', 'user__username', 'user__avatar', 
		'post__id', 'post__image', 'comment__text')

		# Query for user notifications, ordering by notification create time
		notifications = UserNotification.objects.filter(user__username=username).order_by(
		'-notification__create_at').only('is_read', 'notification')

		# Prefetch related notification information using the notification_query
		notifications = notifications.prefetch_related(Prefetch('notification', queryset=notification_query))

		return notifications
