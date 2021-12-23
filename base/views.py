from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from base.forms import RoomForm

from .models import Room
from .models import Topic


# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Lets learn django'},
#     {'id': 3, 'name': 'Lets learn Backend development'},
# ]



def home(request):
    if (request.GET.get('q')!=None):
        q = request.GET.get('q')
    else:
        q= ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'room.html', context)

@login_required(login_url='login')
def createroom(request):
    form = RoomForm()
    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'create-room.html', context)

@login_required(login_url='login')
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if (request.user != room.host):
        return HttpResponse('You are not allowed here')

    if (request.method=='POST'):
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'create-room.html', context)

@login_required(login_url='login')
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)

    if (request.user != room.host):
        return HttpResponse('You are not allowed here')

    if (request.method=='POST'):
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'delete.html', context)


def loginpage(request):
    page = 'login'
    if (request.user.is_authenticated):
        return redirect('home')

    if (request.method=='POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)
        if (user != None):
            login(request, user)
            return redirect('home')
        else:
            messages.error('Username or password does not match')

    context = {'page': page}
    return render(request, 'login-register.html', context)
def registerpage(request):
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'login-register.html', context)
def logoutpage(request):
    logout(request)
    return redirect('home')
    