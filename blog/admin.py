from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import BlogPost

class BlogPostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'short_description', 'slug', 'created_at', 'updated_at')
    list_display_links = ('title',)
    search_fields = ('title', 'short_description', 'content', 'slug')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    summernote_fields = ('content',)
    readonly_fields = ('slug',)

admin.site.register(BlogPost, BlogPostAdmin)
