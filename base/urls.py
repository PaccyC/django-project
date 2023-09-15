from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginView,name='login'),
    path('logout/',views.logoutView,name='logout'),
    path('register/',views.registerView,name='register'),
    path("",views.home,name="home"),
    path("profile/<str:pk>/",views.profile,name="user-profile"),
    path("room/<str:pk>/",views.rooms,name="rooms"),
    path("create-room/",views.createRoom,name="create-room"),
    path("update-room/<str:pk>/",views.updateRoom,name="update-room"),
    path("delete-room/<str:pk>/",views.deleteRoom,name="delete-room"),
    path("delete-message/<str:pk>/",views.deleteMessage,name="delete-message")
]