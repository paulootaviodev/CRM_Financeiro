from .models import BlogPost
from django.views.generic import ListView, DetailView, TemplateView


class BlogHomePage(ListView):
    template_name = 'blog/index.html'
    model = BlogPost
    context_object_name = 'blog_posts'
    paginated_by = 5
    ordering = '-id'


class BlogPost(DetailView):
    template_name = 'blog/post.html'
    model = BlogPost
    context_object_name = 'blog_post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class BlogAbout(TemplateView):
    template_name = 'blog/about.html'
