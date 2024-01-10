from django.urls import path

from . import views

app_name = 'users'


urlpatterns = [
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('registration/', views.UserCreateApiView.as_view(), name='registration'),

    path('profile/', views.ProfileRetrieveUpdate.as_view(), name='profile_by_current_user'),
    path('profile/<int:pk>/', views.ProfileRetrieveUpdate.as_view(), name='profile_by_pk'),

    path('', views.UsersAPIList.as_view(), name='main-page'),
]
