from django.urls import path

from . import views

app_name = 'notices'

urlpatterns = [
    path('notices-list/', views.GetUsersNotifications.as_view(), name='notices-list'),
    path('create-notice-for/<int:pk>/', views.CreateNotification.as_view(), name='create-notice'),
]
