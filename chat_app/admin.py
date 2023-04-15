from django.contrib import admin

from .models import Message, Thread, User


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created')
    readonly_fields = ('update', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'thread', 'text', 'created', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('sender__username', 'receiver__username', 'text')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'password')
