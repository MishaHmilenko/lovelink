from django.contrib import admin

from users.models import EmailConfirmationToken, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'gender')


@admin.register(EmailConfirmationToken)
class EmailConfirmationTokenAdmin(admin.ModelAdmin):
    list_display = ('user',)
