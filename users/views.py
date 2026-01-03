from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth import login, logout

from django.contrib import messages

from .forms import RegisterUserForm

from .forms import LoginUserForm

from base.models import Room, Topic


# Create your views here.
def RegisterView(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created Successfully..!")
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    else:
        form = RegisterUserForm()

    context = {
        'form':form
    }
    return render(request, 'users/register.html', context)

def LoginView(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged In Successfully!")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
    else:
        form = LoginUserForm()

    return render(request, "users/login.html", {"form": form})


def LogoutView(request):

    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method != 'POST':
        return render(request,'405.html', status=405)
    
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


def UserProfile(request, pk):

    user = get_object_or_404(User, id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    context = {
        'user':user,
        'rooms':rooms,
        'topics':topics
    }
    return render(request, "users/profile.html", context)