from rest_framework.permissions import BasePermission


class IsUserProfile(BasePermission):
    message = 'You aren\'t the owner of this profile'

    def has_object_permission(self, request, view, obj):
        print(f"request.user: {request.user}")
        print(f"obj: {obj}")

        if request.method == 'PATCH':
            return request.user == obj.user
        return True

