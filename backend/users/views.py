from datetime import datetime

from django.http import Http404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from users.models import User
from users.serializers import ProfileSerializer, UserSerializer


class UserCreateApiView(generics.CreateAPIView):

    """ Creating user """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApiView(ObtainAuthToken):

    """ Login user """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            return Response(data={'errors': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileRetrieveUpdate(RetrieveUpdateAPIView):

    """ Updating or Retrieving profile """

    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):

        """ Getting object by pk in url or return current user object """

        user_id = self.kwargs.get('pk', None)

        # Returns the current user if there isn't pk
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                print(user)
                return user
            except User.DoesNotExist:
                raise Http404('User does not exists')
        else:
            return self.request.user

    def retrieve(self, request, *args, **kwargs):

        """ Returning profile by get_object() """

        try:
            user = self.get_object()
            serializer = ProfileSerializer(user)
            return Response(serializer.data)
        except Http404 as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):

        """ Updating the profile of the current user """

        user = self.get_object()

        # IF other user try to update current user's profile
        if request.user != user:
            return Response(
            {'error': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersAPIList(ListAPIView):

    """ Getting users by filters """

    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by gender and age
        # Example urls for filters /users/?gender=F

        age_filter = self.request.query_params.get('age', None)
        gender_filter = self.request.query_params.get('gender', None)

        if age_filter is not None:
            min_birth_date = datetime(datetime.now().year - int(age_filter), 1, 1)
            max_birth_date = datetime(datetime.now().year - int(age_filter), 12, 31)
            queryset = queryset.filter(birthday__gte=min_birth_date, birthday__lte=max_birth_date)
        if gender_filter is not None:
            queryset = queryset.filter(gender=gender_filter)

        return queryset
