from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
from .serializers import *
from .models import *

from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import ValidationError
# Create your views here.

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        token_pair = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(token_pair, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = TokenPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class MovieCreateView(generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = MovieSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MovieListView(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class MovieSearchAPIView(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        title = request.data.get('title', None)
        genre = request.data.get('genre', None)
        director = request.data.get('director', None)
        year = request.data.get('year', None)
        keyword = request.data.get('keyword', None)

        movies = Movie.objects.all()

        if keyword:
            movies = movies.filter(Q(title__icontains=keyword) )
        
        if title:
            movies = movies.filter(title__icontains=title)

        if genre:
            movies = movies.filter(genres__name__icontains=genre)

        if director:
            movies = movies.filter(directors__name__icontains=director)

        if year:
            movies = movies.filter(year=year)

        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)