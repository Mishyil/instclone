from django.conf import settings
from django.urls import include, path
from .views import NotificationsView, get_unread_notifications_count, mark_notifications_read
from django.conf.urls.static import static

app_name = 'notifications'


urlpatterns = [
	path('unread-count/', get_unread_notifications_count, name='unread_notifications_count'),
	path('mark-read/', mark_notifications_read, name='mark_notifications_read'),
	path('', NotificationsView.as_view(), name='notifications')
]
