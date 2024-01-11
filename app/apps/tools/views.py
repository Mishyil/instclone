from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect
from main.forms import PhotoUploadForm, AvatarUploadForm, CommentForm
from userpost.models import UserPost
from like.models import PostLike
from userprofile.models import User
from notifications.tasks import create_notification
import uuid


def post_like(request):
	"""
	Handle the like/unlike action for a post.

	Returns:
		JsonResponse: JSON response indicating whether the post was liked or unliked.
	"""
	photo = get_object_or_404(UserPost, id=request.POST.get('photo_id'))
	like_exists = PostLike.objects.filter(user=request.user, post=photo).exists()
	if like_exists:
		PostLike.objects.filter(user=request.user, post=photo).delete()
		liked = False
	else:
		PostLike.objects.create(user=request.user, post=photo)
		liked = True
		create_notification.delay(
			from_profile=request.user.id,
			to_profile=photo.user.id,
			notification_type=1,
			post=photo.id,
		)

	return JsonResponse({'liked': liked})

def upload_photo(request, *args, **kwargs):
	"""
	Handle the photo upload process.

	Returns:
		redirect: Redirect to the user's profile page after a successful photo upload.
	"""
	form = PhotoUploadForm(request.POST, request.FILES)
	if form.is_valid():
		upload_file = request.FILES['file']
		user = request.user
		unique_filename = f'photos/{uuid.uuid4()}.jpg'

		photo = UserPost(user=user)
		photo.image.save(unique_filename, upload_file)
		photo.save()

		create_notification.delay(
			from_profile=user.id,
			notification_type=4,
			post=photo.id,
		)

		return redirect('userprofile:userprofile', username=request.user.username)

def upload_avatar(request, *args, **kwargs):
	"""
	Handle the avatar upload process.

	Returns:
		JsonResponse: JSON response indicating the success of the avatar upload and the new avatar URL.
	"""
	form = AvatarUploadForm(request.POST, request.FILES)
	if form.is_valid():
		upload_file = request.FILES['file']
		user = request.user
		unique_filename = f'avatars/{uuid.uuid4()}.jpg'

		profile = User.objects.get(username=user)
		profile.avatar.save(unique_filename, upload_file)
		profile.save()

		return JsonResponse({
			'success': True,
			'new_avatar_url': profile.avatar.url
		})

def delete_photo(request, *args, **kwargs):
	"""
	Handle the deletion of a photo.

	Returns:
		JsonResponse: JSON response indicating the success of the photo deletion.
	"""
	photo_id = request.POST.get('photo_id')
	photo = UserPost.objects.get(id=photo_id)
	photo.delete()
	return JsonResponse({'success': True})

def follow_profile(request, *args, **kwargs):
	"""
	Handle the follow/unfollow action for a user profile.

	Returns:
		redirect: Redirect to the target user's profile page after the follow/unfollow action.
	"""
	to_profile = User.objects.get(username=request.POST.get('username'))
	from_profile = request.user
	action = request.POST.get('follow')
	if action == 'follow':
		from_profile.follow.add(to_profile)

		create_notification.delay(
			from_profile=from_profile.id,
			to_profile=to_profile.id,
			notification_type=2
		)
	elif action == 'unfollow':
		from_profile.follow.remove(to_profile)
	from_profile.save()
	return redirect('userprofile:userprofile', username=to_profile.username)

def post_comment(request, *args, **kwargs):
	"""
	Handle the posting of a comment on a post.

	Returns:
		HttpResponseRedirect: Redirect to the post's detail page after a successful comment submission.
	"""
	photo_id = request.POST.get('id')
	photo = UserPost.objects.get(id=photo_id)
	form = CommentForm(request.POST)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.post = photo
		comment.user = request.user
		comment.save()

		create_notification.delay(
			from_profile=request.user.id,
			to_profile=photo.user.id,
			notification_type=3,
			post=photo.id,
			comment=comment.id
		)

		return HttpResponseRedirect(f'/p/{photo.id}/')
