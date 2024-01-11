from django.urls import path
from .views import ExploreListView


app_name = 'explore'

urlpatterns = [
	path('', ExploreListView.as_view(), name='explore')
]