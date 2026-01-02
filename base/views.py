from django.shortcuts import render, get_object_or_404, redirect

from .models import Room, Topic

from .forms import RoomForm

from django.db.models import Q

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

def GetRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    context = {
        'room':room
    }
    return render(request, 'base/room.html', context)

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

def UpdateRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    form = RoomForm(instance=room)

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


def DeleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {
        'obj':room
    }
    return render(request, 'base/delete.html', context)
