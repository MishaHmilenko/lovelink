from django.shortcuts import redirect
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response

from chat.models import Chat, Message
from chat.permissions import IsUserInChat
from chat.serializers import ChatCreateSerializer, MessagesFromChatSerializer, MessageFromUserSerializer


class ChatCreateAPIView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatCreateSerializer

    def post(self, request, *args, **kwargs):
        members_data = request.data.get('members', [])
        members_data.append({'id': request.user.id})
        existing_chat = Chat.objects.filter(members=self.request.user).filter(members=members_data[0].get('id')).exists()

        if existing_chat:
            chat = Chat.objects.filter(members=self.request.user).filter(members=members_data[0].get('id'))
            return redirect(f'http://127.0.0.1:8000/chat/{chat.first().id}/')

        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Chat created successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMessagesFromChatAPIView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessagesFromChatSerializer

    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(chat=self.kwargs.get('pk'))

        if len(messages) == 0:
            return Response('Chat is empty', status=status.HTTP_200_OK)

        serializer = MessagesFromChatSerializer(messages, many=True)

        return Response({'messages': serializer.data}, status=status.HTTP_200_OK)


class DeleteChatAPIView(DestroyAPIView):
    queryset = Chat.objects.all()
    permission_classes = [IsUserInChat]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Chat deleted successfully'}, status.HTTP_204_NO_CONTENT)


class CreateMessageAPIView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageFromUserSerializer


class UpdateMessageAPIView(UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageFromUserSerializer


class DeleteMessageAPIView(DestroyAPIView):
    pass
