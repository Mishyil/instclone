from rest_framework.serializers import ModelSerializer
from userpost.models import UserPost


class ExploreSerializer(ModelSerializer):
	
	class Meta:
		model = UserPost
		fields = ['id', 'image']