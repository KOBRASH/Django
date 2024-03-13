from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'published', 'views_count', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
