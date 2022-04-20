from django.contrib import admin
from .models import Post, CommentModel

# Register your models here.

class CommentModelInLine(admin.StackedInline):
    model = CommentModel

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'content')

    inlines = [CommentModelInLine]


admin.site.register(Post, PostAdmin)
