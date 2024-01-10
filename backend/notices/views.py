from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notices.models import NotificationsModel
from notices.serializers import NotificationSerializer
from users.models import User


class CreateNotification(CreateAPIView):

    """ Creating a notice """

    queryset = NotificationsModel.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    # perform_create for add data for fields of database (sender, recipient) after validate all other data
    def perform_create(self, serializer):
        sender = self.request.user
        recipient = get_object_or_404(User, pk=self.kwargs.get('pk'))

        if recipient == sender:
            raise ValidationError('You can\'t send a message to yourself')

        serializer.save(sender=sender, recipient=recipient)


class GetUsersNotifications(ListAPIView):

    """ Getting the first five user notices """

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = NotificationsModel.objects.filter(recipient=user)[:5]
        return queryset
