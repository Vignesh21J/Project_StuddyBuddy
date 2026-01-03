from django.shortcuts import render, get_object_or_404, redirect

from .models import Room, Topic

from .forms import RoomForm

from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Message
# from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

# Create your views here.
def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # print("Search Query:", q)
    # rooms = Room.objects.filter(topic__name__icontains = q)
    topics = Topic.objects.all()

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    room_count = rooms.count()

    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count
    }

    return render(request, 'home.html', context)

@login_required
def GetRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.all().order_by('created')      # reverse lookup
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room':room,
        'room_messages':room_messages,
        'participants':participants
    }
    return render(request, 'base/room.html', context)

@login_required
def CreateRoom(request):

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)

    else:
        form = RoomForm()

    context = {
        'form':form
    }
    return render(request, 'base/room_form.html', context)

@login_required
def UpdateRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        messages.error(request, 'You are not allowed to edit this room.')
        return redirect('room', pk=room.id)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
    context = {
        'form':form
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