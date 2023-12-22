from django.urls import path

from . import views

app_name = 'notices'

urlpatterns = [
    path('create-notice-for/<int:pk>/', views.CreateNotification.as_view(), name='create-notice'),
]
