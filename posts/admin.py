from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    list_filter = ('date_posted', 'author')
    search_fields = ('title', 'content')
    readonly_fields = ('id', 'date_posted', 'slug')
    date_hierarchy = 'date_posted'
    ordering = ('-date_posted',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'date_posted', 'edited_at')
    list_filter = ('date_posted', 'author')
    search_fields = ('content',)
    readonly_fields = ('id', 'date_posted')
    date_hierarchy = 'date_posted'
