from rest_framework.serializers import ModelSerializer
from like.models import PostLike
from api.userprofile.serializers import UserProfileBaseinfoSerializers
from rest_framework import serializers



class PostLikeSerializer(ModelSerializer):
	profile = UserProfileBaseinfoSerializers(read_only=True, source='user')
	user = serializers.HiddenField(default=serializers.CurrentUserDefault())


	class Meta:
		model = PostLike
		fields = ['id', 'profile', 'user']