from django.urls import path
from .views import PhotoView

app_name = 'userpost'

urlpatterns = [
	path('', PhotoView.as_view(), name='userpost')
]
