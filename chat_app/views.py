from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView, RetrieveDestroyAPIView)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import Message, Thread, User
from .serializers import MessageSerializer, ThreadSerializer


class ThreadRetriveAPIView(RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    pagination_class = LimitOffsetPagination

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.filter(pk=kwargs['pk'])
        if user:
            threads = user.first().threads.all()
            serializer = self.get_serializer(threads, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


class ThreadCreateAPIView(CreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        thread = Thread.objects.filter(participants__in=serializer.data['participants'])
        if thread:
            serializer = self.get_serializer(thread.first())
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ThreadDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class MessageCreateAPIView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination


class MessagesRetriveThreadAPIView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination

    def retrieve(self, request, *args, **kwargs):
        thread = Thread.objects.filter(pk=kwargs['pk'])
        if thread:
            messages = thread.first().thread_messages.all()
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


class MessageReadAPIView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def retrieve(self, request, *args, **kwargs):
        message = Message.objects.filter(pk=kwargs['pk'])
        if message:
            message = message.first()
            message.is_read = True
            message.save()
            serializer = self.get_serializer(message)
            return Response(serializer.data)
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


class MessageUnreadAPIView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.filter(pk=kwargs['pk'])
        if user:
            unread_messages = user.first().sent_messages.all().filter(is_read=False).count()
            return Response({'count of unread messages': unread_messages})
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
