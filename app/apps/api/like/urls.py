from django.urls import path, include
from .views import PostLikeAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PostLikeAPIView, basename='likes')


urlpatterns = [
	path('', include(router.urls))
]