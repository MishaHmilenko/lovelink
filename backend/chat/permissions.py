from rest_framework.permissions import BasePermission


class IsUserInChat(BasePermission):
    message = 'You are not a member of chat'

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()
