from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('registration/', views.UserCreateApiView.as_view(), name='registration'),

    path('profile/', views.ProfileRetrieveUpdate.as_view(), name='profile_by_current_user'),
    path('profile/<int:pk>/', views.ProfileRetrieveUpdate.as_view(), name='profile_by_pk'),

    path('', views.UsersProfilesAPIList.as_view(), name='main-page'),

    path('send-confirmation-email/', views.SendEmailConfirmationTokenAPIView.as_view(), name='send-confirmation-email'),
    path('confirm-email/', views.confirm_email_view, name='confirm-email'),

]
