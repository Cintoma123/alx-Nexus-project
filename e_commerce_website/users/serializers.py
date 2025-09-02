from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User , Profile 
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from users.tasks import send_welcome_email


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['phone_number', 'date_of_birth', 'contact_address', 'age']

    def validate_phone_number(self, value):
        """Validate phone number format (basic check)."""
        if value and not value.isdigit() and not (value.startswith('+') and value[1:].isdigit()):
            raise serializers.ValidationError("Phone number must contain only digits and may start with +.")
        if value and len(value) < 7:
            raise serializers.ValidationError("Phone number is too short.")
        return value

    def validate_date_of_birth(self, value):
        """Ensure date of birth is not in the future."""
        if value and value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def validate_age(self, value):
        """Ensure age is reasonable."""
        if value and (value < 0 or value > 120):
            raise serializers.ValidationError("Age must be between 0 and 120.")
        return value

    def validate(self, data):
        """Ensure age matches date_of_birth if both are provided."""
        dob = data.get("date_of_birth")
        age = data.get("age")

        if dob and age:
            today = date.today()
            calculated_age = (
                today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            )
            if abs(calculated_age - age) > 1:  # allow ±1 year for birthday not yet passed
                raise serializers.ValidationError(
                    {"age": "Age does not match the date of birth provided."}
                )
        return data



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
    #Profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username' , 'password2']
        #read_only_fields = ["Profile"]

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
            username=validated_data['username'],
        )
        send_welcome_email(user)
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password' ,"username"]

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        username = data.get('username', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if "username" in self.initial_data:
             raise serializers.ValidationError('An username is not required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')
        user = authenticate(email=email, password=password )
        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')
        
        
        #data['user'] = user
        return {
            "email": user.email,
            #"username": user.username
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

# users/serializers.py


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            # Blacklist the refresh token so it can’t be used again
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


        