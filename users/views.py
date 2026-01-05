from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth import login, logout

from django.contrib import messages

from .forms import RegisterUserForm

from .forms import LoginUserForm

from base.models import Room, Topic

from .forms import EditUserForm
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user
from .models import PasswordReset
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone


# Create your views here.

@unauthenticated_user
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


@unauthenticated_user
def LoginView(request):

    if request.user.is_authenticated:
        return redirect('home')
    
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


def LogoutView(request):

    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method != 'POST':
        return render(request,'405.html', status=405)
    
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')


@login_required
def UserProfile(request, pk):

    user = get_object_or_404(User, id=pk)
    rooms = user.room_set.all()
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


@unauthenticated_user
def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            reset_password_url = reverse('reset-password', kwargs={'reset_id':new_password_reset.reset_id})
            full_reset_password_url = request.build_absolute_uri(reset_password_url)

            email_body = f'Reset your password using the link below:\n\n\n{full_reset_password_url}'

            email_message = EmailMessage(
                'Reset Your Password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]    # List of recipients (receiver email)
            )

            email_message.fail_silently=True
            email_message.send()

            return redirect('reset-password-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"Email sending failed due to incorrect credentials. So Try again with correct credentials!")
            return redirect('forgot-password')

    return render(request, 'users/forgot_password.html')

def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'users/password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')


@unauthenticated_user
def ResetPassword(request, reset_id):
    try:
        reset_entry = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            password_have_error = False

            if password != confirm_password:
                password_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 6:
                password_have_error = True
                messages.error(request, 'Password must be at least 6 characters long')

            expiration_time = reset_entry.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                reset_entry.delete()
                messages.error(request, 'Reset link has expired')
                return redirect('forgot-password')
            
            if not password_have_error:
                user = reset_entry.user
                user.set_password(password)
                user.save()
                reset_entry.delete()
                messages.success(request, 'Password reset. Proceed to login.')
                return redirect('login')
            
            return render(request, 'users/reset_password.html', {'reset_id': reset_entry.reset_id})

    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    
    return render(request, 'users/reset_password.html', {'reset_id':reset_id})