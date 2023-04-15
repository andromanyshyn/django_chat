from django.urls import include, path

from . import views

urlpatterns = [
    path('threads/<int:pk>/',
         views.ThreadRetriveAPIView.as_view(), name='thread_users'),
    # retrieving the list of threads for any user (type threads/user_id into url field)

    path('thread/create/',
         views.ThreadCreateAPIView.as_view(), name='thread_create'),
    # creation of thread, if a thread with particular users exists - we return it

    path('thread/delete/<int:pk>/',
         views.ThreadDestroyAPIView.as_view(), name='thread_delete'),  # removing a thread

    path('message/create/',
         views.MessageCreateAPIView.as_view(), name='message_create'),  # creation of a message

    path('message/thread/<int:pk>/',
         views.MessagesRetriveThreadAPIView.as_view(), name='message_thread'),
    # retrieving message list for the thread (type message/thread/thread_id/ into url field)

    path('message/read/<int:pk>/',
         views.MessageReadAPIView.as_view(), name='message_read'),
    #  marking the message as read (type message/read/message_id/ into url field)

    path('message/unread/<int:pk>/',
         views.MessageUnreadAPIView.as_view(), name='message_unread'),
    # retrieving a number of unread messages for the user
    # (type message/unread/message_id/ into url field) to make it as "read"
]
