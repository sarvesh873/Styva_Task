from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "full_name", "phone","email")
    search_fields = ("username", "phone")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_directors', 'runtime', 'year', 'display_genres')
    search_fields = ("title", )
    def display_directors(self, obj):
        return ', '.join([director.name for director in obj.directors.all()])

    def display_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
