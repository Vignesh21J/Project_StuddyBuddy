from django.shortcuts import render, get_object_or_404, redirect

from .models import Room, Topic

from .forms import RoomForm

from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Message
# from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from .models import MessageFile

# from django.db import connection
# connection.queries.clear()

from django.db.models import Count
from django.db.models import Max
from django.db.models.functions import Coalesce

from django_ratelimit.decorators import ratelimit


# Create your views here.
def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.all()[0:6]

    rooms = (
        Room.objects.select_related('host','topic')
        .prefetch_related('participants')
        .annotate(
            participants_count=Count("participants", distinct=True),
            last_activity=Coalesce(Max('message__created'), 'created')
        )
        .filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
    ).order_by('-last_activity')

    room_count = rooms.count()
    topics_count = Topic.objects.count()

    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,
        'topics_count':topics_count
    }

    return render(request, 'home.html', context)


@login_required
@ratelimit(key='user', rate='20/m', method='POST', block=True)
def GetRoom(request, pk):
    room = get_object_or_404(
        Room.objects
        .select_related("host", "topic")
        .prefetch_related(
            "participants",
            "message_set__user",
            "message_set__files"
        ),
        id=pk
    )

    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()
    

    if request.method == 'POST':

        body = request.POST.get('body').strip()
        uploaded_files = request.FILES.getlist('files')

        ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.mp4', '.mp3', '.wav']
        MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

        errors_found = False

        if not body and not uploaded_files:
            messages.error(request, "You can't send an empty message.")
            return redirect('room', pk=room.id)

        for file in uploaded_files:
            if not any(file.name.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
                errors_found = True
                messages.error(request, f"{file.name} has an unsupported file type.")

            elif file.size > MAX_UPLOAD_SIZE:
                errors_found = True
                messages.error(request, f"{file.name} exceeds maximum size of 10MB.")

        if errors_found:
            return redirect('room', pk=room.id)

        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )

        for file in uploaded_files:
            MessageFile.objects.create(file=file, message=message)


        room.participants.add(request.user)

        return redirect('room', pk=room.id)

    context = {'room':room, 'room_messages':room_messages, 'participants':participants}

    return render(request, 'base/room.html', context)


@login_required
@ratelimit(key='user', rate='30/h', block=True)
def CreateRoom(request):

    topics = Topic.objects.only("id","name")

    if request.method == 'POST':
        topic_name = request.POST.get('topic_entered', '').strip()
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if not topic_name or not name:
            messages.error(request, "Topic and room name are required.")
            return redirect('create-room')

        topic, _ = Topic.objects.get_or_create(name=topic_name)

        room = Room.objects.create(
            host=request.user,
            topic=topic,
            name=name,
            description=description
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)


    form = RoomForm()

    context = {
        'form':form,
        'topics':topics
    }

    return render(request, 'base/room_form.html', context)

@login_required
def UpdateRoom(request, pk):
    room = get_object_or_404(Room, id=pk)

    if request.user != room.host:
        messages.error(request, 'You are not allowed to edit this room.')
        return redirect('room', pk=room.id)

    topics = Topic.objects.only("id", "name")
    form = RoomForm(instance=room)


    if request.method == 'POST':
        topic_name = request.POST.get('topic_entered', '').strip()
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()

        if not topic_name or not name:
            messages.error(request, "Topic and room name are required.")
            return redirect('update-room', pk=room.id)

        topic, _ = Topic.objects.get_or_create(name=topic_name)

        room.name = name
        room.topic = topic
        room.description = description
        room.save()

        return redirect('room', pk=room.id)

    context = {
        'form':form,
        'topics':topics,
        'room':room
    }

    return render(request, 'base/room_form.html', context)



@login_required
def DeleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)

    if request.user != room.host:
        messages.error(request, 'You are not allowed to delete this room.')
        return redirect('room', pk=room.id)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {
        'obj':room
    }
    return render(request, 'base/delete.html', context)

@login_required
def DeleteMessage(request, pk):
    message = get_object_or_404(Message, id=pk)

    if request.user == message.user:
        room_id = message.room.id

        message.delete()
        messages.success(request, "Message deleted.")

        return redirect('room', pk=room_id)
    # else:
    #     return HttpResponseForbidden("You're not allowed to delete this message.")

    raise PermissionDenied



@login_required()
def DeleteFile(request, file_id):
    file = get_object_or_404(MessageFile, id=file_id)

    if file.message.user != request.user:
        raise PermissionDenied

    room_id = file.message.room.id
    file.delete()

    return redirect('room', pk=room_id)



def TopicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = (
        Topic.objects
        .filter(name__icontains=q)
        .annotate(room_count=Count('room'))
    )

    topics_count = topics.count()

    context = {
        'topics':topics,
        'topics_count':topics_count
    }

    return render(request, 'base/topics.html', context)


def ratelimit_blocked(request, exception):
    return render(request, '429.html', status=429)


def AboutView(request):
    return render(request, 'about.html')


def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_403(request, exception):
    return render(request, '403.html', status=403)

def custom_500(request):
    return render(request, '500.html', status=500)
