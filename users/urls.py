from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView, name='login'),
    path('register/', views.RegisterView, name='register'),
    path('logout/', views.LogoutView, name='logout'),

    path('user-profile/<int:pk>/', views.UserProfile, name='user-profile'),
    path('update-user/', views.Updateuser, name='update-user'),

    path('forgot-password', views.ForgotPassword, name="forgot-password"),
    path('password-reset-sent/<uuid:reset_id>/', views.PasswordResetSent, name="reset-password-sent"),
    path('reset-password/<uuid:reset_id>/', views.ResetPassword, name="reset-password"),
]
