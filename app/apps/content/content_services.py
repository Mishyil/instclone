from django.db.models import Count, Prefetch
from userpost.models import UserPost
from userprofile.models import User
from comment.models import Comment
from like.models import PostLike
from django.db.models import Prefetch


def get_filtered_photos(self):
	# Function to retrieve filtered posts for the user's feed

	# Get the current user
	user = self.request.user

	# Get IDs of users the current user is following and include their own ID
	user_ids = list(user.follow.values_list('id', flat=True)) + [user.id]

	# Query for posts filtering by followed users and the current user
	photos = UserPost.objects.filter(user__id__in=user_ids).order_by('-timestamp'
		).prefetch_related(
		# Prefetch user data for each post
		Prefetch('user', 
			queryset=User.objects.only('username', 'avatar'),
			to_attr='custom_user'
		),
		# Prefetch the first two comments for each post with user data for each comment
		Prefetch('comments', 
			queryset=Comment.objects.order_by('-timestamp')[:2].prefetch_related(
				Prefetch('user', 
					queryset=User.objects.only('username'),
					to_attr='custom_user'
				)
			), 
			to_attr='first_two_comments'
		)
	).annotate(likes_count=Count('likes'))

	return photos


def extended_information(self, context, **kwargs):
	# Function to add extended information to the context, such as liked photo IDs for the current user

	# Get the current user
	user = self.request.user

	# Get photo IDs that the user has liked
	context['liked_photo_ids'] = PostLike.objects.filter(user=user).values_list('post_id', flat=True)

	return context

