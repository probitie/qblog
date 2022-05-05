from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile

class ProfileInLine(admin.TabularInline):
    model = Profile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]
    inlines = [ProfileInLine]


admin.site.register(CustomUser, CustomUserAdmin)
