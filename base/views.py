from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

# Create your views here.

def home(request):
    rooms=Room.objects.all()
    context={'rooms':rooms}
    return render(request,'base/home.html',context)

def rooms(request,pk):
    room=Room.objects.get(id=pk)
    context={'room':room}    
    return render(request,'base/room.html',context)  

def createRoom(request):
    form=RoomForm()
    if request.method == 'POST':
        form=RoomForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("home")
            
    context={"form":form}
    return render(request,'base/room_form.html',context)


def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    context={'form':form}
    return render(request,'base/room-form.html',context)


def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})