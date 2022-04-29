from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('profile/<username>', views.profile, name="profile"),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('', include('django.contrib.auth.urls')),
]
