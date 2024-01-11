from .models import Notification, UserNotification
from django.db.models import Prefetch



def filtered_notifications(self):
	# Function to retrieve filtered notifications for the current authenticated user

	# Get the current user
	user = self.request.user

	# Define the prefetch query for related notification data
	notification_prefetch = Prefetch(
		'notification', 
		queryset=Notification.objects.order_by('create_at'
			).select_related('user', 'post', 'comment')
	)

	# Query for user notifications, ordered by notification creation timestamp in descending order
	notifications = UserNotification.objects.filter(user=user
		).order_by('-notification__create_at').prefetch_related(
		notification_prefetch
	)

	return notifications