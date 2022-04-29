from django.contrib import admin
from django.urls import path
from django.urls import include

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='main'),
    path('add_post', views.add_post, name='add_post'),
    path('publish_post/<slug>', views.publish_post, name='publish_post'),
    path('delete_post/<slug>', views.delete_post, name='delete_post'),
    path('search/', views.search_post_form, name='search'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
