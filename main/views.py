from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import FollowRequest, Video, Comment, Profile
from .forms import VideoForm, CommentForm, ProfileForm, ShareVideoForm
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.template.loader import render_to_string

import mediapipe as mp
import cv2
from . import poseEstimation


def home(request):
    # Initialize an empty queryset to build upon based on user state
    videos = Video.objects.none()

    if request.user.is_authenticated:
        # For authenticated users, get videos from followed users
        followed_users = request.user.profile.following.all()
        followed_videos = Video.objects.filter(user__in=followed_users)

        # Get public videos excluding those from followed users to avoid duplicates
        public_videos = Video.objects.filter(user__profile__is_private=False).exclude(user__in=followed_users)

        # Combine queries and order by the upload date
        videos = (followed_videos | public_videos).order_by('-upload_date')
    else: 
        # For anonymous users, only show public videos
        videos = Video.objects.filter(user__profile__is_private=False).order_by('-upload_date')

    return render(request, 'main/home.html', {'videos': videos})


def video_detail(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    comments = video.comments.all().order_by('-created_at')
    return render(request, 'main/video_detail.html', {'video': video, 'comments': comments})

def video_view(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    seen_videos = request.session.get('seen_videos', [])
    if video_id not in seen_videos:
        seen_videos.append(video_id)
        request.session['seen_videos'] = seen_videos
    return render(request, 'main/video_detail.html', {'video': video})

 

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def get_pose_landmarks(image):
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        return landmarks
    return None

def analyze_video(video_path, exercise):
    cap = cv2.VideoCapture(video_path)
    alignment_results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        landmarks = get_pose_landmarks(frame)
        if landmarks:
            alignment_status = poseEstimation.check_alignment(landmarks, exercise)
            alignment_results.append(alignment_status)
    
    cap.release()
    
    # Determine overall analysis based on majority results
    if alignment_results:
        proper_alignment_count = alignment_results.count("Proper Alignment")
        if proper_alignment_count / len(alignment_results) > 0.8:
            return "Proper Alignment"
        else:
            return "Improper Alignment"
    return "No Pose Detected"

@login_required
def add_videos(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video_instance = form.save(commit=False)
            video_instance.user = request.user

            # Process the video file to extract pose analysis
            video_path = video_instance.file.path
            cap = cv2.VideoCapture(video_path)
            pose_landmarks = []
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                landmarks = get_pose_landmarks(frame)
                if landmarks:
                    pose_landmarks.append(landmarks)
            cap.release()

            if pose_landmarks:
                exercise_name = video_instance.exercise_name
                is_proper_alignment = poseEstimation.check_alignment(pose_landmarks, exercise_name)
                video_instance.analysis = "Proper Alignment" if is_proper_alignment else "Improper Alignment"
            else:
                video_instance.analysis = "Pose landmarks not detected"

            video_instance.save()
            return redirect('profile', username=request.user.username)
    else:
        form = VideoForm()

    return render(request, 'main/add_videos.html', {'form': form})

@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_own_profile = request.user == profile_user
    is_following = request.user.profile.followers.filter(id=profile_user.id).exists()
    can_view_videos = is_own_profile or not profile_user.profile.is_private or is_following

    # Retrieve videos based on the visibility
    if can_view_videos:
        videos = Video.objects.filter(user=profile_user)
    else:
        videos = Video.objects.none()

    # Gather counts of followers and following
    followers_count = profile_user.profile.followers.count()
    following_count = User.objects.filter(profile__followers=profile_user).count()  # Assuming a reverse relation from User to Profile for followers
    bio = profile_user.profile.bio

    context = {
        'profile_user': profile_user,
        'followers_count': followers_count,
        'following_count': following_count,
        'bio': bio,
        'videos': videos,
        'is_own_profile': is_own_profile,
        'can_view_videos': can_view_videos,
    }

    return render(request, 'main/profile.html', context)

@login_required
def follow_user(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = profile_user.profile
    if profile.is_private:
        if not FollowRequest.objects.filter(from_user=request.user, to_user=profile_user).exists():
            FollowRequest.objects.create(from_user=request.user, to_user=profile_user)
    else:
        profile.followers.add(request.user)
    return redirect('profile', username=username)

@login_required
def notifications(request):
    follow_requests = FollowRequest.objects.filter(to_user=request.user)
    return render(request, 'main/notifications.html', {'follow_requests': follow_requests})

@login_required
def accept_follow_request(request, request_id):
    follow_request = get_object_or_404(FollowRequest, id=request_id)
    follow_request.to_user.profile.followers.add(follow_request.from_user)
    follow_request.delete()
    return redirect('notifications')

@login_required
def decline_follow_request(request, request_id):
    follow_request = get_object_or_404(FollowRequest, id=request_id)
    follow_request.delete()
    return redirect('notifications')


@login_required
def followers_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers = profile_user.profile.followers.all()
    return render(request, 'main/followers_list.html', {'profile_user': profile_user, 'followers': followers})

@login_required
def following_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    following = profile_user.profile.following
    return render(request, 'main/following_list.html', {'profile_user': profile_user, 'following': following})

@login_required
def remove_follower(request, username, follower_id):
    profile_user = get_object_or_404(User, username=username)
    follower = get_object_or_404(User, id=follower_id)
    if request.user == profile_user or request.user == follower:
        profile_user.profile.followers.remove(follower)
        messages.success(request, f'You have removed {follower.username}.')
    return redirect('followers_list', username=username)

@login_required
def unfollow_user(request, username, followee_id):
    followee = get_object_or_404(User, id=followee_id)
    if request.user.profile.followers.filter(id=followee.id).exists() or followee.profile.followers.filter(id=request.user.id).exists():
        request.user.profile.followers.remove(followee)
        followee.profile.followers.remove(request.user)
        messages.success(request, f'You have unfollowed {followee.username}.')
    return redirect('following_list', username=username)


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'main/update_profile.html', {'profile_form': profile_form})

@login_required
def shared_videos(request):
    shared_videos = Video.objects.filter(shared_with=request.user)
    return render(request, 'main/shared_videos.html', {'shared_videos': shared_videos})

@login_required
def share_video(request, video_id):
    video = get_object_or_404(Video, id=video_id, user=request.user)
    if request.method == 'POST':
        share_form = ShareVideoForm(request.POST, video=video)
        if share_form.is_valid():
            share_form.save()
            return redirect('profile', username=request.user.username)
    else:
        share_form = ShareVideoForm()

    return render(request, 'main/share_video.html', {'video': video, 'share_form': share_form})

@login_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id, user=request.user)
    if request.method == 'POST':
        video.delete()
        return redirect('profile', username=request.user.username)

    return render(request, 'main/delete_video.html', {'video': video})

@login_required
def add_comment(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(user=request.user, video=video, text=comment_text)
        return redirect('home', video_id=video_id)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.video.user:
        comment.delete()
    return redirect('profile', username=request.user.username)

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
    else:
        comment.likes.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home')) 


def search(request):
    query = request.GET.get('q')
    if not query:
        return render(request, 'main/search_results.html', {'results': []})

    users = User.objects.filter(username__icontains=query)
    videos = Video.objects.filter(exercise_name__icontains=query, user__profile__is_private=False)

    # Exclude private users' videos unless the user is authenticated and follows them
    if request.user.is_authenticated:
        private_videos = Video.objects.filter(exercise_name__icontains=query, user__profile__is_private=True)
        followed_users = request.user.profile.following.all()
        videos = videos | private_videos.filter(user__in=followed_users)

    context = {
        'query': query,
        'users': users,
        'videos': videos,
    }
    return render(request, 'main/search_results.html', context)