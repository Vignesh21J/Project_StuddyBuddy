from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url:
            return next_url
        return resolve_url('home')



from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
User = get_user_model()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if request.user.is_authenticated:
            return

        email = sociallogin.user.email
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.user = user
            except User.DoesNotExist:
                pass


    def get_login_redirect_url(self, request):
        next_url = request.GET.get('next') or request.POST.get('next')
        if next_url:
            return next_url
        return resolve_url('home')