from django.contrib import admin
from .models import UserProfile, FriendRequest

admin.site.register(UserProfile)
admin.site.register(FriendRequest)