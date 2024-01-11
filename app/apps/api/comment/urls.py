from django.urls import path, include
from .views import CommentListAPIView
from rest_framework.routers import DefaultRouter

# URL for displaying and managing comments in the individual UserPost object.
router = DefaultRouter()
router.register(r'', CommentListAPIView, basename='comment')


urlpatterns = [
	path('', include(router.urls))
]