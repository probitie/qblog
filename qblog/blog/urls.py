from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='main'),
    path('add_post', views.add_post, name='add_post'),
    path('publish_post/<slug>', views.publish_post, name='publish_post'),
    path('delete_post/<slug>', views.delete_post, name='delete_post'),
    path('search_post/', views.search_post, name='search'),
    path('view_post/<slug:slug>/', views.post_detail, name='post_detail'),
]
