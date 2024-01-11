from django.contrib import admin
from userpost.models import UserPost
from userprofile.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)


admin.site.register(UserPost)





