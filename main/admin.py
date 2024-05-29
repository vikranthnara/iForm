from django.contrib import admin
from .models import Video, Profile, Comment, FollowRequest

admin.site.register(Video)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(FollowRequest)


# Register your models here.
