from django.contrib import admin
from .models import Room, Message, Topic

# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    search_fields = [
        'name',
    ]


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