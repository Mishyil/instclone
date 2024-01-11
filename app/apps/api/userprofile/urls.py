from django.urls import path, include
from .views import UserProfileRetriveAPIView
from .views import UserFollowersListAPIView, UserFollowingListAPIView


urlpatterns = [
	# Endpoint for retrieving the user's own profile information.
	path('profile/', UserProfileRetriveAPIView.as_view({'get': 'retrieve', 'patch': 'partial_update'})),

	# Includes URLs from the 'api.content.urls', likely for managing and viewing user posts.
	path('postfeed/', include('api.content.urls')),

	# Includes URLs from the 'api.userpost.urls', presumably for managing and viewing user-specific posts.
	path('posts/', include('api.userpost.urls')),

	# Includes URLs from the 'api.notification.urls', possibly for managing and viewing user notifications.
	path('notification/', include('api.notification.urls')),

	# Endpoint for retrieving the list of followers for the user.
	path('followers/', UserFollowersListAPIView.as_view()),

	# Endpoint for retrieving the list of users whom the user is following.
	path('following/', UserFollowingListAPIView.as_view()),
]