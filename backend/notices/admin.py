from django.contrib import admin

from notices.models import NotificationsModel


@admin.register(NotificationsModel)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient')
