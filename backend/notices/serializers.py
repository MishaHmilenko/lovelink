from rest_framework import serializers

from notices.models import NotificationsModel


class NotificationSerializer(serializers.ModelSerializer):

    """ Serializer for notices """

    class Meta:
        model = NotificationsModel
        fields = ('message',)

