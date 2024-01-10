from django.shortcuts import get_object_or_404
from rest_framework import serializers

from chat.models import Chat, Message
from users.models import User


class SimpleUserSerializer(serializers.Serializer):

    """ Serializer for validating only id """

    id = serializers.IntegerField()


class ChatCreateSerializer(serializers.ModelSerializer):

    """ Serializer for creating chat by user id """

    members = SimpleUserSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('members',)

    def create(self, validated_data):
        members_data = validated_data.pop('members', [])
        chat = Chat.objects.create()

        # Add users to chat
        for member_data in members_data:
            user_instance = User.objects.get(id=member_data['id'])
            chat.members.add(user_instance)

        return chat


class MessagesFromChatSerializer(serializers.ModelSerializer):

    """ Serializer for getting messages from users """
    class Meta:
        model = Message
        fields = ('user', 'content')


class MessageFromUserSerializer(serializers.ModelSerializer):

    """ Serializer for message from user """

    class Meta:
        model = Message
        fields = ('content',)

    def create(self, validated_data):
        chat = get_object_or_404(Chat, pk=self.context['view'].kwargs.get('pk'))
        return Message.objects.create(user=self.context['request'].user, chat=chat, **validated_data)


