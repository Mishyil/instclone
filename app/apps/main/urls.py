from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'main'

urlpatterns = [
	path('favicon.ico/', views.favicon, name='favicon'),
	path('register/', views.UserRegisterView.as_view(), name='register'),
	path('login/', views.UserLoginView.as_view(), name='login'),
	path('', views.get_template, name='home'),


]

