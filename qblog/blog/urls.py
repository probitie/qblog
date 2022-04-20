from django.contrib import admin
from django.urls import path
from django.urls import include

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('search/', views.search_post_form, name='search'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
