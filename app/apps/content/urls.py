from django.urls import path
from .views import ContentView

app_name = 'content'

urlpatterns = [
	path('', ContentView.as_view(), name='content')
]