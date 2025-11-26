from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Event, Profile, Wishlist


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'created_at', 'updated_at')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at', 'updated_at')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at')
    list_filter = ('name', 'user')
    ordering = ('-created_at',)
