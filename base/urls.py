from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('room/<int:pk>', views.GetRoom, name="room"),
    path('create-room/', views.CreateRoom, name="create-room"),
    path('update-room/<int:pk>/', views.UpdateRoom, name="update-room"),
    path('delete-room/<int:pk>/', views.DeleteRoom, name="delete-room"),

    path('delete-message/<int:pk>', views.DeleteMessage , name='delete-message'),
    path('delete-file/<int:file_id>/', views.DeleteFile, name='delete-file'),

    path('topics/', views.TopicPage , name="topics"),
]
