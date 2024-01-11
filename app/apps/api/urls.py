from django.urls import path, include
from api.main.views import UserLogInAPIView, UserLogOutAPIView, UserRegisterAPIView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # path('logout/', UserLogOutAPIView.as_view()),
    # path('register/', UserRegisterAPIView.as_view()),
    # path('login/', UserLogInAPIView.as_view()),
    path('token/', obtain_auth_token, name='api_token_auth'),
    path('<slug:username>/', include('api.userprofile.urls')),
    path('', include('api.main.urls')),
]