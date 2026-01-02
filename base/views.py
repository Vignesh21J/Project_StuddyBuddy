from django.shortcuts import render, get_object_or_404

from .models import Room

# Create your views here.
def Home(request):
    rooms = Room.objects.all()
    context = {
        'rooms':rooms
    }

    return render(request, 'home.html', context)

def GetRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    context = {
        'room':room
    }
    return render(request, 'base/room.html', context)