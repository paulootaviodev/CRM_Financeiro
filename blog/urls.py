from django.urls import path
from .views import BlogHomePage, BlogPost, BlogAbout

urlpatterns = [
    path('', BlogHomePage.as_view(), name='blog_home_page'),
    path('post/<slug:slug>/', BlogPost.as_view(), name='blog_post'),
    path('about/', BlogAbout.as_view(), name='blog_about'),
]
