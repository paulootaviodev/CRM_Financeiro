from datetime import date
from PIL import Image

from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

from blog.models import BlogPost, ViewsPerMonth
from ._base import BaseClassForTestCaseTesting


class BlogPostModelTest(BaseClassForTestCaseTesting):
    """Tests for the BlogPost model."""

    def test_slug_is_unique(self):
        """Validates whether the generated slug is truly unique."""

        self.assertIsNotNone(self.post1.slug)
        self.assertIsNotNone(self.post2.slug)
        self.assertNotEqual(self.post1.slug, self.post2.slug)
        
        with self.assertRaises(IntegrityError):
            self.post2.slug = self.post1.slug
            self.post2.save()
    
    def test_missing_model_data(self):
        """Test if model raises ValidationError if some field is missing"""

        image = self._create_dummy_image(10, 10, name='test_3.jpg')

        data = {
            'title': 'Test Title',
            'short_description': 'A short test description.',
            'content': 'This is the body of the blog post.',
            'featured_image': image
        }

        for field in data.keys():
            with self.subTest(field=field):
                missing_data = data.copy()
                del missing_data[field]

                with self.assertRaises(ValidationError):
                    post3 = BlogPost(**missing_data)
                    post3.full_clean()

    def test_image_is_resized_if_too_large(self):
        """Validates whether the image is resized if it is larger than 1920x1080."""

        large_image = self._create_dummy_image(3000, 2000, name='large.jpg')

        self.post1.featured_image = large_image
        self.post1.save()
        self.post1.refresh_from_db()

        with Image.open(self.post1.featured_image.path) as img:
            width, height = img.size
            self.assertLessEqual(width, 1920)

            expected_height = int(width / (16/9))
            self.assertEqual(height, expected_height)

    def test_image_has_16_9_aspect_ratio(self):
        """Validates whether the final image is in 16:9 format."""

        square_image = self._create_dummy_image(1000, 1000, name='square.jpg')

        self.post1.featured_image = square_image
        self.post1.save()
        self.post1.refresh_from_db()
        
        with Image.open(self.post1.featured_image.path) as img:
            width, height = img.size
            aspect_ratio = width / height

            self.assertAlmostEqual(aspect_ratio, 16/9, places=2)

    def test_invalid_image_format_raises_error(self):
        """Validates whether invalid image formats (e.g. GIF) cause an error."""

        gif_image = self._create_dummy_image(100, 100, name='test_4.gif', img_format='GIF')

        with self.assertRaises(ValidationError):
            self.post1.featured_image = gif_image
            self.post1.save()

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

                self.post1.featured_image = image
                self.post1.save()
                self.post1.refresh_from_db()

                self.assertTrue(self.post1.featured_image.storage.exists(self.post1.featured_image.name))
                # The process_image() function will convert any image to .jpg format.
                self.assertTrue(self.post1.featured_image.name.lower().endswith(f'.jpg'))
    
    def test_image_larger_than_5mb_is_not_accepted(self):
        """Images larger than 5mb is not accepted."""

        large_image = self._create_dummy_image(100, 100, name=f'test_size.jpg', size_in_mb=6)

        with self.assertRaises(ValidationError):
            self.post1.featured_image = large_image
            self.post1.save()


class ViewsPerMonthModelTest(BaseClassForTestCaseTesting):
    """Tests for the ViewsPerMonth model."""

    def test_unique_together_constraint(self):
        """Validates the unique constraint for (post, month)."""
        
        test_month = date(2025, 9, 1)
        ViewsPerMonth.objects.create(post=self.post1, month=test_month, total=100)

        # Try to create an entry for the same post and same month
        with self.assertRaises(
            IntegrityError,
            msg="It shouldn't be possible to create two entries for the same post and month."
        ):
            ViewsPerMonth.objects.create(post=self.post1, month=test_month, total=50)

    def test_allows_different_months_for_same_post(self):
        """Validates that it is possible to create entries for different months in the same post."""
        
        month1 = date(2025, 9, 1)
        month2 = date(2025, 10, 1)
        ViewsPerMonth.objects.create(post=self.post1, month=month1, total=100)
        
        try:
            ViewsPerMonth.objects.create(post=self.post1, month=month2, total=200)
        except IntegrityError:
            self.fail("It should be possible to create entries for different months in the same post.")
        
        self.assertEqual(ViewsPerMonth.objects.filter(post=self.post1).count(), 2)
