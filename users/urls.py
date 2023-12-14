from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('registration/', views.UserCreateApiView.as_view(), name='registration'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
