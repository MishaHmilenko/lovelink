from datetime import date, datetime

from django.http import Http404
from django.shortcuts import render

from django_filters import rest_framework as filters

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.filters import UsersProfilesFilter
from users.models import EmailConfirmationToken, User
from users.serializers import ProfileSerializer, UserSerializer
from users.utils import send_confirmation_email


class UserCreateApiView(generics.CreateAPIView):

    """ Creating user """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def calculate_age(self, birthdate):
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            age = self.calculate_age(datetime.strptime(request.data.get('birthday'), '%Y-%m-%d'))
            serializer.validated_data['age'] = age
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
        print(request.user)

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


class UsersProfilesAPIList(ListAPIView):

    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UsersProfilesFilter


# class UsersAPIList(ListAPIView):
#
#     """ Getting users by filters """
#
#     queryset = User.objects.all()
#     serializer_class = ProfileSerializer
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#
#         # Filter by gender and age
#         # Example urls for filters /users/?gender=F
#
#         age_filter = self.request.query_params.get('age', None)
#         gender_filter = self.request.query_params.get('gender', None)
#
#         if age_filter is not None:
#             min_birth_date = datetime(datetime.now().year - int(age_filter), 1, 1)
#             max_birth_date = datetime(datetime.now().year - int(age_filter), 12, 31)
#             queryset = queryset.filter(birthday__gte=min_birth_date, birthday__lte=max_birth_date)
#         if gender_filter is not None:
#             queryset = queryset.filter(gender=gender_filter)
#
#         return queryset


class SendEmailConfirmationTokenAPIView(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request):
        user = request.user

        if EmailConfirmationToken.objects.filter(user=user).first():
            return Response(data={'detail': 'The confirmation token already exists'}, status=status.HTTP_400_BAD_REQUEST)

        token = EmailConfirmationToken.objects.create(user=user)
        send_confirmation_email(email=user.email, user=user, token_id=token.id)
        return Response(data={'detail': 'The confirmation token was created'}, status=status.HTTP_201_CREATED)


def confirm_email_view(request):
    token_id = request.GET.get('token_id', None)
    try:
        token = EmailConfirmationToken.objects.get(pk=token_id)
        user = token.user
        user.is_email_confirmed = True
        user.save()
        return render(
            request,
            template_name='users/email_confirmation.html',
            context={'is_email_confirmed': True}
        )

    except EmailConfirmationToken.DoesNotExist:
        return render(
            request,
            template_name='users/email_confirmation.html',
            context={'is_email_confirmed': False}
        )



