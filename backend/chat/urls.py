from django.urls import path

from chat import views

app_name = 'chat'


urlpatterns = [
    path('create/', views.ChatCreateAPIView.as_view(), name='chat-create'),
    path('delete/<int:pk>/', views.DeleteChatAPIView.as_view(), name='chat-delete'),
    path('<int:pk>/', views.GetMessagesFromChatAPIView.as_view(), name='chat'),

    path('<int:pk>/create-message/', views.CreateMessageAPIView.as_view(), name='create-message'),
    path('update-message/<int:pk>/', views.UpdateMessageAPIView.as_view(), name='update-message'),
    path('delete-message/<int:pk>/', views.DeleteMessageAPIView.as_view(), name='delete-message'),

]
