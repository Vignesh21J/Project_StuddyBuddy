from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView, name='login'),
    path('register/', views.RegisterView, name='register'),
    path('logout/', views.LogoutView, name='logout'),

    path('user-profile/<int:pk>/', views.UserProfile, name='user-profile'),
    path('update-user/', views.Updateuser, name='update-user'),
]
