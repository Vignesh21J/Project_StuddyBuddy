from django.urls import path
from . import views

urlpatterns = [
    path('room/<int:pk>', views.GetRoom, name="room"),
    path('create-room/', views.CreateRoom, name="create-room"),
    path('update-room/<int:pk>/', views.UpdateRoom, name="update-room"),
    path('delete-room/<int:pk>/', views.DeleteRoom, name="delete-room"),
]
