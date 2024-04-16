from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path('movies/', MovieCreateView.as_view(), name='movie-list'),
    path('movieslist/', MovieListView.as_view(), name='movie-list'),
    path('search/', MovieSearchAPIView.as_view(), name='movie-search'),
    # path("profile/", ProfileView.as_view(), name="profile"),
    # path('logout/', LogoutAPIView.as_view(), name="logout"),
]