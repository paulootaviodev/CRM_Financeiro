from blog.forms import BlogPostForm
from django.test import TestCase
from ._base import ImageMixin
from PIL import Image


class BlogFormsTest(ImageMixin, TestCase):
    """Test whether the form is validating the fields correctly."""

    def test_valid_form_data(self):
        """Test is form is valid with valid data"""

        image = self._create_dummy_image(10, 10, name="test_form.jpg")

        data = {
        'title': 'Test Title',
        'short_description': 'A short test description.',
        'content': 'This is the body of the blog post.',
        }
        file_data = {'featured_image': image}
        
        form = BlogPostForm(data=data, files=file_data)
        
        # Assert that the form is valid
        self.assertTrue(form.is_valid())
        
        # Check if the cleaned data contains the processed image
        self.assertEqual(form.cleaned_data['featured_image'].name, 'test_form.jpg')
    
    def test_missing_form_data(self):
        """Test is form is invalid with missing data"""

        image = self._create_dummy_image(10, 10, name="test_form.jpg")

        data = {
        'title': 'Test Title',
        'short_description': 'A short test description.',
        'content': 'This is the body of the blog post.',
        }
        file_data = {'featured_image': image}

        for field in data.keys():
            missing_data = data.copy()
            del missing_data[field]

            form = BlogPostForm(data=missing_data, files=file_data)

            # Assert that the form is invalid
            self.assertFalse(form.is_valid())
        
        form = BlogPostForm(data=data)
        # Assert that the form is invalid
        self.assertFalse(form.is_valid())
    
    def test_image_is_resized_if_too_large(self):
        """Validates whether the image is resized if it is larger than 1920x1080."""

        large_image = self._create_dummy_image(3000, 2000, name='large.jpg')

        data = {
        'title': 'Test Title',
        'short_description': 'A short test description.',
        'content': 'This is the body of the blog post.',
        }
        file_data = {'featured_image': large_image}

        form = BlogPostForm(data=data, files=file_data)
        self.assertTrue(form.is_valid())

        with Image.open(form.cleaned_data['featured_image']) as img:
            width, height = img.size
            self.assertLessEqual(width, 1920)

            expected_height = int(width / (16/9))
            self.assertEqual(height, expected_height)

    def test_image_has_16_9_aspect_ratio(self):
        """Validates whether the final image is in 16:9 format."""

        square_image = self._create_dummy_image(1000, 1000, name='square.jpg')

        data = {
        'title': 'Test Title',
        'short_description': 'A short test description.',
        'content': 'This is the body of the blog post.',
        }
        file_data = {'featured_image': square_image}

        form = BlogPostForm(data=data, files=file_data)
        self.assertTrue(form.is_valid())
        
        with Image.open(form.cleaned_data['featured_image']) as img:
            width, height = img.size
            aspect_ratio = width / height

            self.assertAlmostEqual(aspect_ratio, 16/9, places=2)

    def test_invalid_image_format_raises_error(self):
        """Validates whether invalid image formats (e.g. GIF) cause an error."""

        gif_image = self._create_dummy_image(100, 100, name='test_4.gif', img_format='GIF')

        data = {
            'title': 'Test Title',
            'short_description': 'A short test description.',
            'content': 'This is the body of the blog post.',
            }
        file_data = {'featured_image': gif_image}

        form = BlogPostForm(data=data, files=file_data)
        # Assert that the form is invalid
        self.assertFalse(form.is_valid())

    def test_valid_image_formats_are_accepted(self):
        """Validates whether JPG, JPEG, and PNG formats are accepted and processed."""

        formats = {
            'jpeg': 'JPEG',
            'jpg': 'JPEG',
            'png': 'PNG'
        }

        for ext, fmt in formats.items():
            with self.subTest(format=ext):
                image = self._create_dummy_image(100, 100, name=f'test_5.{ext}', img_format=fmt)

                data = {
                    'title': 'Test Title',
                    'short_description': 'A short test description.',
                    'content': 'This is the body of the blog post.',
                    }
                file_data = {'featured_image': image}

                form = BlogPostForm(data=data, files=file_data)
                self.assertTrue(form.is_valid())

                # The process_image() function will convert any image to .jpg format.
                self.assertTrue(form.cleaned_data['featured_image'].name.lower().endswith(f'.jpg'))
    
    def test_image_larger_than_5mb_is_invalid(self):
        """Images larger than 5mb are invalid."""

        image = self._create_dummy_image(100, 100, name=f'test_size.jpg', size_in_mb=6)

        data = {
            'title': 'Test Title',
            'short_description': 'A short test description.',
            'content': 'This is the body of the blog post.',
            }
        file_data = {'featured_image': image}

        form = BlogPostForm(data=data, files=file_data)
        self.assertFalse(form.is_valid())
