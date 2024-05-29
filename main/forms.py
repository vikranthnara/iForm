from django import forms
from .models import Video, Comment, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['exercise_name', 'file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': 'video/mp4'}),
        }

class ShareVideoForm(forms.Form):
    username = forms.CharField(max_length=150, label='Share with User')

    def __init__(self, *args, **kwargs):
        video = kwargs.pop('video', None)
        super().__init__(*args, **kwargs)
        self.video = video

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')
        return user

    def save(self):
        user = self.cleaned_data['username']
        self.video.shared_with.add(user)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'is_private']
