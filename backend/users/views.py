from django.views.generic import TemplateView
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(data={'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApiView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(data={'errors': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(TemplateView):
    template_name = 'users/success.html'
