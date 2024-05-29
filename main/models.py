from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    exercise_name = models.CharField(max_length=50)
    analysis = models.CharField(max_length=50)
    file = models.FileField(upload_to='videos/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    shared_with = models.ManyToManyField(User, related_name='shared_videos', blank=True)
    upload_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.exercise_name


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return f'Comment by {self.user} on {self.video}'
    
    @property
    def total_likes(self):
        return self.likes.count()
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    seen_videos = models.ManyToManyField(Video, related_name='seen_by', blank=True)

    
    def __str__(self):
        return self.user.username

    @property
    def following(self):
        return User.objects.filter(profile__followers=self.user)

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class FollowRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='follow_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='follow_requests_received', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"