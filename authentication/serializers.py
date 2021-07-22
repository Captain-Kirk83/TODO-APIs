from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=500)


class LoginSerializer(serializers.Serializer):
    # TODO: Implement login functionality
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        username=attrs['username']
        password=attrs['password']
        if username and password:
            user=authenticate(request=None,username=username,password=password)
            if user:
                if user.is_active:
                    attrs['user']=user
                else:
                    message='Account is disabled'
                    raise exceptions.ValidationError(message)
            else:
                message='Either username or password is wrong'
                raise exceptions.ValidationError(message)
        else:
            message='Both fields must be filled'
            raise exceptions.ValidationError(message)
        return super().validate(attrs)


class RegisterSerializer(serializers.Serializer):
    # TODO: Implement register functionality
    username=serializers.CharField(max_length=150)
    first_name=serializers.CharField(max_length=150)
    last_name=serializers.CharField(max_length=150)
    email=serializers.EmailField()
    password1=serializers.CharField(style={'input_type':'password'}, write_only=True)
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)

    def validate(self, attrs):
        username=attrs['username']
        first_name=attrs['first_name']
        last_name=attrs['last_name']
        email=attrs['email']
        password1=attrs['password1']
        password2=attrs['password2']
        if username and first_name and last_name and email and password1 and password2:
            user=User.objects.filter(username=username)
            if user:
                message='User already created'
                raise exceptions.ValidationError(message)
            if password1 != password2:
                message='Both passwords must be same'
                raise exceptions.ValidationError(message)
        else:
            message='All fields must be filled'
            raise exceptions.ValidationError(message)
        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    # TODO: Implement the functionality to display user details
    class Meta:
        model=User
        fields=['id','username','email','first_name','last_name']
    