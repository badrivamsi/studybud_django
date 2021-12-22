from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

rooms = [
    {'id': 1, 'name': 'Lets learn python'},
    {'id': 2, 'name': 'Lets learn django'},
    {'id': 3, 'name': 'Lets learn Backend development'},
]

def home(request):
    context = {'rooms': rooms}
    return render(request, 'home.html', context)

def room(request, pk):
    room = None
    for i in rooms:
        if i['id']==int(pk):
            room = i
            break
    context = {'room': room}
    return render(request, 'room.html', context)