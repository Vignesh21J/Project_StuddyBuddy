from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth import login, logout

from django.contrib import messages

from .forms import RegisterUserForm

from .forms import LoginUserForm

from base.models import Topic

from .forms import EditUserForm
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user
from django.db.models import Count


from django_ratelimit.decorators import ratelimit

from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST


# Create your views here.

@unauthenticated_user
def RegisterView(request):

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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


@unauthenticated_user
@ratelimit(key='ip', rate='8/m', block=True)
def LoginView(request):

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged In Successfully!")

            if next_url:
                return redirect(resolve_url(next_url))

            return redirect("home")

        else:
            messages.error(request, "Invalid email or password")
    else:
        form = LoginUserForm()

    context = {
        "form": form,
        "next": next_url
    }

    return render(request, "users/login.html", context)


@require_POST
def LogoutView(request):

    if not request.user.is_authenticated:
        return redirect('login')

    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


@login_required
def UserProfile(request, pk):

    user = get_object_or_404(User, id=pk)

    rooms = (
        user.room_set
        .select_related("host", "topic")
        .prefetch_related("participants")
        .annotate(participants_count=Count("participants"))
    )

    rooms_count = rooms.count()
    topics = Topic.objects.all()

    context = {
        'user':user,
        'rooms':rooms,
        'topics':topics,
        'rooms_count':rooms_count
    }
    return render(request, "users/profile.html", context)


@login_required
def Updateuser(request):
    user = request.user

    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully!.")
            return redirect('user-profile', pk=user.id)

        messages.error(request, "Error occured while updating..!")

    else:
        form = EditUserForm(instance=user)

    context = {
        'form':form
    }

    return render(request, "users/update_user.html", context)