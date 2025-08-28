from .models import BlogPost
from django.views.generic import ListView, DetailView, TemplateView
from django.http import JsonResponse
from utils.request_rate_limit import rate_limited_view


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

    def post(self, request, *args, **kwargs):
        # Rate-limiting check
        rate_limit_response = rate_limited_view(request)
        if rate_limit_response:
            return JsonResponse({"success": False}, status=429)

        blog_post = self.get_object()
        blog_post.views += 1
        blog_post.save(update_fields=["views"])
        return JsonResponse({"success": True}, status=200)


class BlogAbout(TemplateView):
    template_name = 'blog/about.html'
