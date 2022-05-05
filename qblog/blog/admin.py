from django.contrib import admin
from .models import Post, Comment

class CommentModelInLine(admin.StackedInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'content')

    inlines = [CommentModelInLine]


admin.site.register(Post, PostAdmin)
