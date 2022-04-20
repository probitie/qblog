from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import *


app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]
