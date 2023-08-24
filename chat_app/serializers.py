from django.contrib.auth import get_user_model
from rest_framework import serializers

from chat_app.models import Message, Thread

User = get_user_model()


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.SlugRelatedField(
        slug_field="username", many=True, queryset=User.objects.all()
    )

    class Meta:
        model = Thread
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Message
        fields = "__all__"
