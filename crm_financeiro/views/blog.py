from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import BlogPostForm
from blog.models import BlogPost


class CreateBlogPost(LoginRequiredMixin, CreateView):
    template_name = "crm_financeiro/create_blog_post.html"
    model = BlogPost
    form_class = BlogPostForm

    def get_success_url(self):
        return reverse("detail_blog_post", kwargs={"slug": self.object.slug})

class ListBlogPosts(LoginRequiredMixin, ListView):
    template_name = "crm_financeiro/list_blog_posts.html"
    context_object_name = "blog_posts"
    model = BlogPost
    paginate_by = 50
    ordering = '-id'


class DetailBlogPost(LoginRequiredMixin, DetailView):
    template_name = "crm_financeiro/detail_blog_post.html"
    context_object_name = "blog_post"
    model = BlogPost
    slug_field = "slug"
    slug_url_kwarg = "slug"


class EditBlogPost(LoginRequiredMixin, UpdateView):
    template_name = "crm_financeiro/update_blog_post.html"
    context_object_name = "blog_post_form"
    model = BlogPost
    form_class = BlogPostForm
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return reverse("detail_blog_post", kwargs={"slug": self.object.slug})
