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

# Create your views here.
def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # print("Search Query:", q)
    # rooms = Room.objects.filter(topic__name__icontains = q)
    topics = Topic.objects.all()[0:6]

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

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
def GetRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
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
def CreateRoom(request):

    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic_entered')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room = Room.objects.create(
            host = request.user,
            topic = topic,

            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        room.participants.add(request.user)
        return redirect('home')

    else:
        form = RoomForm()

    context = {
        'form':form,
        'topics':topics
    }

    return render(request, 'base/room_form.html', context)

@login_required
def UpdateRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    form = RoomForm(instance=room)

    topics = Topic.objects.all()

    if request.user != room.host:
        messages.error(request, 'You are not allowed to edit this room.')
        return redirect('room', pk=room.id)

    if request.method == 'POST':
        topic_name = request.POST.get('topic_entered')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', room.id)
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

    if file.message.user == request.user:
        file.delete()
    
    return redirect('room', pk=file.message.room.id)



def TopicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)

    topics_count = topics.count()

    context = {
        'topics':topics,
        'topics_count':topics_count
    }

    return render(request, 'base/topics.html', context)
