from django.contrib import admin

from chat_app.models import Message, Thread


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "updated")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "thread", "text", "created", "is_read")
    list_filter = ("is_read", "created")
    search_fields = ("sender__username", "sender__email")
