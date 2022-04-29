from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class ProfileInLine(admin.TabularInline):
    model = Profile


class ProfileUserAdmin(UserAdmin):
    inlines = [ProfileInLine]


admin.site.register(User, ProfileUserAdmin)
# Register your models here.
