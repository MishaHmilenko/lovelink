from django.contrib import admin

from chat.models import Chat, Message


@admin.register(Chat)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('display_members',)

    def display_members(self, obj):
        return 'Chat: ' + ', '.join([str(member) for member in obj.members.all()])

    display_members.short_description = 'Members'


admin.site.register(Message)