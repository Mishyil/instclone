from django.urls import path
from .views import NotificationListAPIView


# URL for view notifications current user
urlpatterns = [
	path('', NotificationListAPIView.as_view())
]