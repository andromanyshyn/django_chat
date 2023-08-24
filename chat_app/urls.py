from django.urls import include, path
from rest_framework.routers import DefaultRouter

from chat_app import views

router = DefaultRouter()
router.register("threads", views.ThreadViewSet, basename="threads")
router.register("messages", views.MessageViewSet, basename="messages")

urlpatterns = [
    path("", include(router.urls)),
]
