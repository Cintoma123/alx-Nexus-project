from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


User = get_user_model()


class ProfileuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username' , 'email']



class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and cannot be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    password2 = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'username' , 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('password and confirm password does not match')
        return attrs

    def create (self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            #token=validated_data['token'],
            username=validated_data['username'],
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        #data['user'] = user
        return {
            "email": user.email,
            "username": user.username
        }




class ChangepasswordSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    new_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    new_password2 = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
            model = User
            fields = ['old_password' , 'new_password' ,'new_password2']
    
    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password2 = attrs.get('new_password2')
        #user = self.context.get('user')
        if new_password != new_password2:
            raise serializers.ValidationError('Password and Confirm Password do not match')
        return attrs


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
    

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

        