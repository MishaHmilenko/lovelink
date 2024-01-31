from rest_framework.permissions import BasePermission


class IsSenderOrResipient(BasePermission):
    message = 'You\'re not a sender or rcipient'

    def has_object_permission(self, request, view, obj):
        return request.user in [obj.sender, obj.recipient]
