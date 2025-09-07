import io
import os
import shutil
import tempfile
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from blog.models import BlogPost

# Creates a temporary bucket for test media files
MEDIA_ROOT_TEST = tempfile.mkdtemp()


class ImageMixin:
    """Mixin to handle image-related test utilities."""

    @classmethod
    def tearDownClass(cls):
        """Clears the temporary media folder after all tests in the class have run."""

        super().tearDownClass()
        if os.path.exists(MEDIA_ROOT_TEST):
            shutil.rmtree(MEDIA_ROOT_TEST)
    
    @staticmethod
    def _create_dummy_image(width, height, name='test.jpg', img_format='JPEG', size_in_mb=None):
        """Creates a fake image in memory for testing."""
        file_io = io.BytesIO()

        if size_in_mb:
            # Calculate a scale factor to increase the image dimensions.
            scale_factor = (size_in_mb * 1024 * 1024) / (width * height * 3) # 3 bytes per pixel for RGB
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = Image.new('RGB', size=(new_width, new_height), color='blue')
        else:
            image = Image.new('RGB', size=(width, height), color='blue')

        image.save(file_io, format=img_format)

        file_io.seek(0)
        return SimpleUploadedFile(name, file_io.read(), content_type=f'image/{img_format.lower()}')


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class BaseClassForTestCaseTesting(ImageMixin, TestCase):
    """Base class that can be used in all TestCase tests."""

    @classmethod
    def setUpTestData(cls):
        # Creates two blog posts that will be used by all tests in this test case
        dummy_image = cls._create_dummy_image(10, 10, name='test_2.jpg')
        cls.post1 = BlogPost.objects.create(
            title='Test Title 1',
            short_description='Description 1',
            content='Content 1',
            featured_image=dummy_image
        )
        cls.post2 = BlogPost.objects.create(
            title='Test Title 2',
            short_description='Description 2',
            content='Content 2',
            featured_image=dummy_image
        )
        cls.post1.refresh_from_db()
        cls.post2.refresh_from_db()


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class BaseClassForLiveServerTesting(ImageMixin, LiveServerTestCase):
    """Base class that can be used in all LiveServerTestCase tests."""

    def setUp(self):
        """Initial setup for each individual test."""

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        dummy_image = self._create_dummy_image(10, 10, name='test_7.jpg')
        self.post = BlogPost.objects.create(
            title='Blog Context Test',
            short_description='Blog Short Description Test',
            content='Blog Content Test',
            featured_image=dummy_image
        )

        self.post.refresh_from_db()

    def tearDown(self):
        """Terminates the driver after each test."""
        self.driver.quit()
