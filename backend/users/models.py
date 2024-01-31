from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
    ]
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    is_email_confirmed = models.BooleanField(default=False)
    coins = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.username


class EmailConfirmationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Token for {self.user}'
