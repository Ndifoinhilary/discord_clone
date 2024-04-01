from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rooms.forms import CreateRoomForm
from rooms.models import Room, Topic, Message
from pprint import pprint
# Create your views here.


def HomeView(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)).order_by('-created')
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'rooms/index.html', context)


def RoomView(request, id):
    room = get_object_or_404(Room, pk=id)
    conversations = room.rooms.order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        body = request.POST.get('body')
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=body
        )
        room.participants.add(request.user)
        return redirect('rooms:room', id=room.id)
    context = {'room': room, 'conversations': conversations,
               'participants': participants}

    return render(request, 'rooms/room.html', context)


@login_required(login_url='core:login')
def CreateRoomView(request):

    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms:home')

    else:
        form = CreateRoomForm()
    context = {'form': form}

    return render(request, 'rooms/create_form.html', context)


# TODO: add a custom permission only for host users to edit room
@login_required(login_url='core:login')
def UpdateRoomView(request, id):
    instance = get_object_or_404(Room, pk=id)
    if request.user != instance.host:
        return HttpResponse("You are not allowed to update this room")
    if request.method == 'POST':
        form = CreateRoomForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('rooms:home')

    else:
        form = CreateRoomForm(instance=instance)

    context = {'form': form}

    return render(request, 'rooms/create_form.html', context)


# TODO: add a custom permission only for host users to delete room
@login_required(login_url='core:login')
def DeleteRoomView(request, id):
    room = get_object_or_404(Room, pk=id)
    if request.user != room.host:
        return HttpResponse("You are not allowed to delete this room")
    if request.method == 'POST':
        room.delete()
        return redirect('rooms:home')

    context = {'obj': room}

    return render(request, 'delete.html', context)


def DeleteMessage(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('rooms:room', id=message.room.id)

    context = {'obj': message}

    return render(request, 'delete.html', context)
