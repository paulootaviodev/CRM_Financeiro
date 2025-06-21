from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'short_description', 'featured_image', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
