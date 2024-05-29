from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from main.models import Profile


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            return redirect("/")  # Redirect to home or any other page you prefer after registration
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('/')

 