from django.urls import path, include
from .views import UserRegisterAPIView, UserLogInAPIView, UserLogOutAPIView

urlpatterns = [
	path('register/', UserRegisterAPIView.as_view(),
		name='user-register'),  # Endpoint for user registration
	path('login/', UserLogInAPIView.as_view(),
		name='user-login'),     # Endpoint for user login
	path('logout/', UserLogOutAPIView.as_view(),
		name='user-logout'),    # Endpoint for user logout
	path('explore/', include('api.explore.urls'))
]
