from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from userprofile.serializers import ProfileSerializer
from users.models import User


class ProfileUpdate(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        print('user', self.request.user)
        serializer = ProfileSerializer(self.request.user)
        return Response(serializer.data)
