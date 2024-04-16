from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import *
from datetime import datetime

class TokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = [
            "username", 
            "first_name",
            "last_name",
            "password", 
            "email", 
            "phone", 
            ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, value):
        validate_password(value)
        return value
    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists.')
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists.')
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user