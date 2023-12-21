from django.urls import path
from .views import ProfileUpdate


app_name = 'userprofile'

urlpatterns = [
    path('', ProfileUpdate.as_view(), name='profile_by_current_user'),
    path('<int:pk>/', ProfileUpdate.as_view(), name='profile_by_pk')
]
