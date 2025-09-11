from django.test import Client
from django.urls import reverse
from ._base import BaseClassForTestCaseTesting


class BlogURLsTest(BaseClassForTestCaseTesting):
    """Tests for blog URLs."""

    def test_blog_home_page_url_status_code_200_ok(self):
        client = Client()
        response = client.get(reverse("blog_home_page"))
        self.assertEqual(response.status_code, 200)
    
    def test_blog_post_url_status_code_200_ok(self):
        client = Client()
        response = client.get(reverse("blog_post", kwargs={"slug": self.post1.slug}))
        self.assertEqual(response.status_code, 200)

    def test_blog_about_url_status_code_200_ok(self):
        client = Client()
        response = client.get(reverse("blog_about"))
        self.assertEqual(response.status_code, 200)
