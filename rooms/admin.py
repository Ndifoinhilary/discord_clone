from django.contrib import admin

from rooms.models import Room, Message, Topic

# Register your models here.





@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name',]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['body']


admin.site.register(Topic)