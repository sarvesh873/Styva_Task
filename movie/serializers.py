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


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all(), many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'runtime', 'year', 'directors', 'genres']

    def create(self, validated_data):
        directors_data = validated_data.pop('directors')
        genres_data = validated_data.pop('genres')

        movie = Movie.objects.create(**validated_data)

        for director in directors_data:
            movie.directors.add(director)

        for genre in genres_data:
            movie.genres.add(genre)

        return movie

    def to_internal_value(self, data):
        data_copy = data.copy()
        directors = data_copy.pop('directors', [])
        genres = data_copy.pop('genres', [])

        director_pks = [Director.objects.get_or_create(name=director_name)[0].pk for director_name in directors]
        genre_pks = [Genre.objects.get_or_create(name=genre_name)[0].pk for genre_name in genres]

        data_copy['directors'] = director_pks
        data_copy['genres'] = genre_pks

        return super().to_internal_value(data_copy)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['directors'] = [director.name for director in instance.directors.all()]
        representation['genres'] = [genre.name for genre in instance.genres.all()]
        return representation