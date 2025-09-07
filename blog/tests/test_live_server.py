import time

from ._base import BaseClassForLiveServerTesting
from django.urls import reverse
from selenium.webdriver.common.by import By


class BlogSeleniumE2ETest(BaseClassForLiveServerTesting):
    """Performs tests with LiveServerTestCase on blog posts."""

    def test_view_count_increases_after_3_seconds_selenium(self):
        """
        Checks if the view count increases after the user
        remains on the page for more than 3 seconds (via JavaScript).
        """

        # Captures the initial state of the views BEFORE the action.
        self.initial_views = self.post.views

        post_url = f"{self.live_server_url}{reverse("blog_post", kwargs={"slug": self.post.slug})}"

        # Simulate user visit and wait
        self.driver.get(post_url)
        self.driver.execute_script("return document.readyState") == "complete"
        time.sleep(4)

        # Check if the database has been updated
        self.post.refresh_from_db()
        final_views = self.post.views

        self.assertEqual(
            final_views,
            self.initial_views + 1,
            f"View count failed. Expected: {self.initial_views + 1}, Found: {final_views}"
        )
    
    def test_blog_home_page_context_is_displayed(self):
        """Test if the blog home page context is displayed."""

        self.driver.get(f"{self.live_server_url}{reverse("blog_home_page")}")
        page_content = self.driver.find_element(By.TAG_NAME, "body").text

        self.assertIn(self.post.title, page_content)
        self.assertIn(self.post.short_description, page_content)
    
    def test_blog_post_context_is_displayed(self):
        """Test if the blog post page context is displayed."""

        self.driver.get(f"{self.live_server_url}{reverse('blog_post', kwargs={'slug': self.post.slug})}")
        page_content = self.driver.find_element(By.TAG_NAME, "body").text
        image_url = self.driver.find_element(By.CLASS_NAME, "masthead").get_attribute('style')

        self.assertIn(self.post.title, page_content)
        self.assertIn(self.post.short_description, page_content)
        self.assertIn(self.post.content, page_content)
        self.assertIn(self.post.featured_image.url, image_url)
