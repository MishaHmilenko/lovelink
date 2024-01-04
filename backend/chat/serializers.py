from rest_framework import serializers

from chat.models import Chat, Message
from users.models import User


class SimpleUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ChatCreateSerializer(serializers.ModelSerializer):
    members = SimpleUserSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('members',)

    def create(self, validated_data):
        members_data = validated_data.pop('members', [])
        chat = Chat.objects.create()

        for member_data in members_data:
            user_instance = User.objects.get(id=member_data['id'])
            chat.members.add(user_instance)

        return chat


class MessagesFromChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('user', 'content')


class MessageFromUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('chat', 'content')
        read_only_fields = ('chat',)

    def create(self, validated_data):
        return Message.objects.create(user=self.context['request'].user, **validated_data)

