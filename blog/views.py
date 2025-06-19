from django.views.generic import TemplateView


class BlogHomePage(TemplateView):
    template_name = 'blog/index.html'


class BlogPost(TemplateView):
    template_name = 'blog/post.html'


class BlogAbout(TemplateView):
    template_name = 'blog/about.html'
