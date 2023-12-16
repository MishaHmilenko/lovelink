from django.urls import path
from .views import ProfileUpdate


app_name = 'userprofile'

urlpatterns = [
    path('', ProfileUpdate.as_view())
]
