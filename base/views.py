from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic,Message,User
from .forms import RoomForm, UserForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout


# Create your views here.

def loginView(request):
    page='login'
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username=request.POST.get("username").lower()
        password=request.POST.get("password")
        
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User not found")   
        user = authenticate(request,username=username,password=password)    
        if user is not None:
            login(request,user)
            return redirect('home') 
        else :
            messages.error(request,"Username OR password not found")
            
    return render(request,'base/login-register.html',{"page":page})

def logoutView(request):
    logout(request)
    return redirect('home')

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q) |
                              Q(description__icontains=q) |
                              Q(title__icontains=q)
                              
                              ) 
    topics=Topic.objects.all()[0:5]
    room_count=rooms.count()
    messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context={'rooms':rooms,'topics':topics,
             'room_count':room_count, 'room_messages':messages}
    return render(request,'base/home.html',context)

def rooms(request,pk):
    room=Room.objects.get(id=pk)
    messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method == 'POST':
       new_message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
           
        )
       room.participants.add(request.user)
       return redirect('room')
    context={'room':room,'messages':messages,'participants':participants}    
    return render(request,'base/room.html',context)  

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method == 'POST':
        
     topic_name= request.POST.get('topic')
     topic, created= Topic.objects.get_or_create(name=topic_name)
    
     Room.objects.create(
        host=request.user,
        topic=topic,
        title=request.POST.get('title'),
        description=request.POST.get('description'),
    )
     return redirect("home")
            
    context={"form":form,"topics":topics}
    return render(request,'base/create-room.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        
     topic_name= request.POST.get('topic')
     topic, created= Topic.objects.get_or_create(name=topic_name)
     room.title= request.POST.get("title")
     room.topic= topic
     room.description=request.POST.get("description")
     room.title=request.POST.get("title") 
     room.save()
    context={'form':form,"topics":topics,'room':room}
    return render(request,'base/room-form.html',context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


def registerView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")
    else:
        form = UserCreationForm()
    
    return render(request,'base/login-register.html', {"form": form})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed here")
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


def profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    messages= user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'messages':messages,'topics':topics}
    return  render(request,'base/profile.html',context)

@login_required(login_url='login')
def updateUser(request):
    user= request.user
    form= UserForm(instance=user)
    
    if request.method == 'POST':
        form= UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk =user.id)
    return render(request,'base/update-user.html',{'form':form})


def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'base/topics.html',{'topics':topics})
    
    
def activityPage(request):
    room_messages= Message.objects.all()
    return  render(request,'base/activity.html',{'messages':room_messages})   
    