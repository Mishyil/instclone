from rest_framework.serializers import ModelSerializer
from api.userprofile.serializers import UserProfileSerializer
from userpost.models import UserPost
from api.comment.serializers import CommentSerializers, CommentContentSerializers
from rest_framework import serializers



class ContentModelSerializer(ModelSerializer):
	"""
	Serializer for displaying feedpost current user.

	"""
	profile = UserProfileSerializer(read_only=True, source='user')
	comments = CommentContentSerializers(many=True ,read_only=True)
	current_user_liked = serializers.BooleanField(read_only=True)
	likes_count = serializers.IntegerField(read_only=True)
	
	class Meta:
		model = UserPost
		fields = ['profile', 'image', 'caption', 'timestamp', 'comments', 'current_user_liked', 'likes_count']

	def to_representation(self, instance):
		representation = super(ContentModelSerializer, self).to_representation(instance)
		representation['comments'] = representation['comments'][:2]
		return representation