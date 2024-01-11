from django.urls import path
from .views import ContentListAPIView

# URL for displaying feedpost current user
urlpatterns = [
	path('', ContentListAPIView.as_view()),
]