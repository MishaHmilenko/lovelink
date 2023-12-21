from django.http import Http404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from userprofile.serializers import ProfileSerializer
from users.models import User


class ProfileUpdate(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        user_id = self.kwargs.get('pk', None)

        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                return user
            except User.DoesNotExist:
                raise Http404('User does not exists')
        else:
            return self.request.user

    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = ProfileSerializer(user)
            return Response(serializer.data)
        except Http404 as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()

        if request.user != user:
            return Response(
            {'error': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProfileSerializer(self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
