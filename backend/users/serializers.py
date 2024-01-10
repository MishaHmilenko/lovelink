from datetime import date

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    """ Serializer for User data """

    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):

        """ Checking if data from user is valid """

        if not self.validate_age(data['birthday']):
            raise serializers.ValidationError('You must be over 10 years old')

        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password do not match')

        return data

    def create(self, validated_data):

        """ Method for creating user by his data """

        # Deleting fields password1 and password2 and add validate password to database field password
        password = validated_data.pop('password1', None)
        validated_data.pop('password2', None)

        try:
            user = User.objects.create_user(**validated_data, password=password)
        except Exception as e:
            errors = {'errors': str(e)}
            raise serializers.ValidationError(errors)

        return user

    def validate_age(self, birthdate):

        """ Method for checking is user age is valid """

        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return 10 < age

    class Meta:
        model = User
        fields = ('username', 'birthday', 'gender', 'email', 'phone_number', 'password1', 'password2')


class ProfileSerializer(serializers.ModelSerializer):

    """ Serializer for user's profile """

    class Meta:
        model = User
        fields = ('username', 'birthday', 'bio', 'gender', 'image')

        extra_kwargs = {
            # Fields can be not required
            field: {'required': False} for field in fields
        }
