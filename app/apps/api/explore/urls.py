from django.urls import path
from .views import ExploreAPIView


urlpatterns = [
	path('', ExploreAPIView.as_view(), name='explore')
]