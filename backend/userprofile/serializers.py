from rest_framework import serializers

from users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'birthday', 'bio', 'gender', 'image')

        extra_kwargs = {
            field: {'required': False} for field in fields
        }
