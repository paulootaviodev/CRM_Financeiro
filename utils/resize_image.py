from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO

def process_image(image):
    """
    Resize and crop large images to maintain the 16/9 aspect ratio and maximum resolution of 1920x1080.
    This process is performed in memory before saving the image to storage.
    """
    valid_extensions = ['jpg', 'jpeg', 'png']
    filename = image.name.lower()

    if not any(filename.endswith(ext) for ext in valid_extensions):
        raise ValidationError("A imagem deve estar em formato JPG, JPEG ou PNG.")
    
    if image.size > 5 * 1024 * 1024:
        raise ValidationError("A imagem não pode ultrapassar 5MB.")

    try:
        with Image.open(image).convert('RGB') as img:
            width, height = img.size
            target_ratio = 16 / 9
            current_ratio = width / height

            if current_ratio > target_ratio:
                # wider image → crop on the sides
                new_width = int(height * target_ratio)
                left = (width - new_width) // 2
                img = img.crop((left, 0, left + new_width, height))

            elif current_ratio < target_ratio:
                # taller image → crop top/bottom
                new_height = int(width / target_ratio)
                top = (height - new_height) // 2
                img = img.crop((0, top, width, top + new_height))

            # Resize to 1920x1080 if image is larger
            if img.width > 1920 or img.height > 1080:
                img = img.resize((1920, 1080), Image.Resampling.LANCZOS)

            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=60)
            buffer.seek(0)

            return InMemoryUploadedFile(
                buffer,
                'ImageField',
                f"{image.name.split('.')[0]}.jpg",
                'image/jpeg',
                buffer.getbuffer().nbytes,
                None
            )

    except Exception as e:
        raise ValidationError(f"Erro ao processar a imagem. Erro: {e}")
