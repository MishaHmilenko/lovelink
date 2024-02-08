from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat.models import Chat, Message
from chat.permissions import IsUserInChat, IsUserOwnerMessage
from chat.serializers import (ChatCreateSerializer, MessageFromUserSerializer,
                              MessagesFromChatSerializer)
from users.models import User


class ChatCreateAPIView(CreateAPIView):

    """ Creating chat if it doesn't exist """

    queryset = Chat.objects.all()
    serializer_class = ChatCreateSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):
        members_data = request.data.get('members', [])
        members_data.append({'id': request.user.id})

        try:
            User.objects.get(pk=members_data[0].get('id'))
        except User.DoesNotExist as e:
            return Response(data={'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        # Checking chat exist
        existing_chat = Chat.objects.filter(members=self.request.user).filter(members=members_data[0].get('id')).exists()

        if existing_chat:
            chat = Chat.objects.filter(members=self.request.user).filter(members=members_data[0].get('id'))
            return redirect(reverse('chat:chat', kwargs={'pk': chat.first().id}))

        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Chat created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMessagesFromChatAPIView(RetrieveAPIView):

    """ Getting all messages from chat """

    queryset = Chat.objects.all()
    serializer_class = MessagesFromChatSerializer
    permission_classes = [IsUserInChat,]

    def get(self, request, *args, **kwargs):
        chat = self.get_object()
        messages = Message.objects.filter(chat=chat)

        if len(messages) == 0:
            return Response('Chat is empty', status=status.HTTP_200_OK)

        serializer = MessagesFromChatSerializer(messages, many=True)

        return Response({'messages': serializer.data}, status=status.HTTP_200_OK)


class DeleteChatAPIView(DestroyAPIView):

    """ Deleting chat """

    queryset = Chat.objects.all()
    permission_classes = [IsUserInChat]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Chat deleted successfully'}, status.HTTP_204_NO_CONTENT)


class CreateMessageAPIView(CreateAPIView):

    """ Creating message """

    queryset = Chat.objects.all()
    serializer_class = MessageFromUserSerializer
    permission_classes = [IsUserInChat]

    def post(self, request, *args, **kwargs):
        self.get_object()
        return self.create(request, *args, **kwargs)


class UpdateMessageAPIView(UpdateAPIView):

    """ Updating user message"""

    queryset = Message.objects.all()
    serializer_class = MessageFromUserSerializer
    permission_classes = [IsUserOwnerMessage]


class DeleteMessageAPIView(DestroyAPIView):

    """ Deleting message """

    queryset = Message.objects.all()
    permission_classes = [IsUserOwnerMessage]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Message deleted successfully'}, status.HTTP_204_NO_CONTENT)
