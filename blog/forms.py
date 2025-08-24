from .models import BlogPost
from utils.resize_image import process_image
from django import forms
from django_summernote.widgets import SummernoteWidget

class BlogPostForm(forms.ModelForm):
    title = forms.CharField(
        label="Título:",
        widget=forms.TextInput(attrs={
            'id': 'title',
            'class': 'form-control'
        }),
        required=True
    )

    short_description = forms.CharField(
        label="Descrição curta:",
        widget=forms.TextInput(attrs={
            'id': 'short_description',
            'class': 'form-control'
        }),
        required=True
    )

    featured_image = forms.ImageField(
        label="Imagem destacada",
        widget=forms.FileInput(attrs={
            'type': 'file',
            'class': 'form-control',
            'id': 'featured_image',
            'name': 'featured_image',
            'placeholder': 'Imagem destacada',
            'style': 'opacity: 0; width: 0; padding: 0; margin: 0; height: 0; pointer-events: none',
        }),
        required=True
    )
    
    class Meta:
        model = BlogPost
        fields = ("title", "short_description", "featured_image", "content")
        widgets = {
            'content': SummernoteWidget(),
        }
    
    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        if image:
            image = process_image(image)

        return image
