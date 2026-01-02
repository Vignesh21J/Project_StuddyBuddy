from django.contrib import admin
from .models import Room, Message

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

    search_fields = [
        'name',
        'description'
    ]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'room',
        'body'
    ]
    search_fields = [
        'body',
        'user',
        'room',
    ]