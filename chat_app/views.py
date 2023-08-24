from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chat_app.models import Message, Thread
from chat_app.serializers import MessageSerializer, ThreadSerializer


class ThreadViewSet(ModelViewSet):
    """GET - /threads/ - Get All Threads for the User
    POST - /threads/ - Creation of a thread, if it exists then just return it
    PUT - /threads/<pk>/ - Put request
    PATCH - /threads/<pk>/ - Patch request
    DELETE - /threads/<pk>/ - Delete a thread
    GET - /threads/<pk>/messages/ - Retrieve List of messages for the Thread
    """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.request.user.threads.all()

    def create(self, request, *args, **kwargs):
        thread = Thread.objects.filter(
            participants__in=request.data["participants"]
        ).first()
        if thread:
            serializer = self.get_serializer(thread)
            return Response(serializer.data)
        else:
            response = super().create(request, *args, *kwargs)
            return Response(response.data, status=response.status_code)

    @action(detail=True, methods=["GET"])
    def messages(self, request, pk):
        thread = self.get_object()
        messages = Message.objects.filter(thread=thread)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(ModelViewSet):
    """GET - /messages/ - Get All messages
    GET - /messages/<pk> - Get and read the message
    POST - /messages/ - Creation of a message
    PUT - /messages/<pk>/ - Put request
    PATCH - /messages/<pk>/ - Patch request
    DELETE - /messages/<pk>/ - Delete a message
    GET - /messages/unread_messages/ - Retrieve count of unread messages for the user
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.is_read:
            instance.is_read = True
            instance.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def unread_messages(self, request):
        count_messages = self.queryset.filter(
            sender=request.user, is_read=False
        ).count()
        data = {"unread_messages": count_messages}
        return Response(data)
