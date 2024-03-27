from django.urls import path, re_path
from .views import HomeView,RoomView, CreateRoomView,UpdateRoomView,DeleteRoomView

app_name = 'rooms'

urlpatterns = [
    path('', HomeView, name='home'),
    path('room/details/<int:id>/', RoomView, name='room'),
    path('room/create/', CreateRoomView, name='room-create'),
    path('room/update/<int:id>/', UpdateRoomView, name='room-update'),
    path('room/delete/<int:id>/', DeleteRoomView, name='delete-room'),

]