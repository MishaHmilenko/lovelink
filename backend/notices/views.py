from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notices.models import NotificationsModel
from notices.serializers import NotificationSerializer
from users.models import User


class CreateNotification(CreateAPIView):
    queryset = NotificationsModel.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        sender = self.request.user
        recipient = get_object_or_404(User, pk=self.kwargs.get('pk'))

        serializer.save(sender=sender, recipient=recipient)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class GetUsersNotifications(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = NotificationsModel.objects.filter(recipient=user)[:5]
        return queryset
