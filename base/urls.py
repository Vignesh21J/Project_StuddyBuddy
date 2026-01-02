from django.urls import path
from . import views

urlpatterns = [
    path('room/<int:pk>', views.GetRoom, name="room")
]
