from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), 
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    path('add-videos/', views.add_videos, name='add_videos'),
    path('share-video/<int:video_id>/', views.share_video, name='share_video'),
    path('delete-video/<int:video_id>/', views.delete_video, name='delete_video'),
    path('profile/<str:username>/', views.profile, name='profile'), 
    path('shared-videos/', views.shared_videos, name='shared_videos'),
    path('add-comment/<int:video_id>/', views.add_comment, name='add_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('notifications/', views.notifications, name='notifications'),  # Add this line
    path('accept-follow-request/<int:request_id>/', views.accept_follow_request, name='accept_follow_request'),
    path('decline-follow-request/<int:request_id>/', views.decline_follow_request, name='decline_follow_request'),
    path('followers/<str:username>/', views.followers_list, name='followers_list'),
    path('following/<str:username>/', views.following_list, name='following_list'),
    path('remove-follower/<str:username>/<int:follower_id>/', views.remove_follower, name='remove_follower'),
    path('unfollow-user/<str:username>/<int:followee_id>/', views.unfollow_user, name='unfollow_user'),
    path('search/', views.search, name='search'),


] 
