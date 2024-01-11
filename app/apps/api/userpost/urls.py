from django.urls import path, include
from .views import UserPostAPIView, ProfileUserPosts

urlpatterns = [
	# URL for displaying a list of posts in the user's profile
	path('', ProfileUserPosts.as_view({
		'get': 'list',
		'post': 'create'
	})),

	# URL for displaying, creating, updating, and deleting a specific post
	path('<int:pk>/', UserPostAPIView.as_view({
		'get': 'retrieve',          # Retrieve a specific post
		'patch': 'partial_update',  # Partially update a post
		'delete': 'destroy'         # Delete a specific post
	})),

	# URL for displaying the list of comments related to a specific post
	path('<int:post_pk>/comments/', include('api.comment.urls')),
	path('<int:post_pk>/likes/', include('api.like.urls')),
]