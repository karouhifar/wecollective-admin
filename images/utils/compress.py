from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO


class CompressedImageS3Storage(S3Boto3Storage):
    def _save(self, name, content):
        if name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            try:
                img = Image.open(content)
                if img.mode in ('RGBA', 'LA'):
                    img = img.convert('RGB')

                buffer = BytesIO()
                format = 'JPEG' if name.lower().endswith(
                    ('.jpg', '.jpeg')) else 'PNG' if name.lower().endswith('.png') else 'WEBP'
                img.save(buffer, format=format, quality=85, optimize=True)
                buffer.seek(0)

                content = ContentFile(buffer.read())
                content.name = name
            except Exception as e:
                print(f"Compression failed, uploading original: {e}")
                content.seek(0)

        return super()._save(name, content)
