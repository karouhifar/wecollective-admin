
import os
from django.db import models
from django.db.models import Q
from images.utils.compress import CompressedImageS3Storage
from wecollectiveadmin.settings import AWS_CLOUDFRONT_DOMAIN
# Create your models here.


class ImageUpload(models.Model):
    """
    Model to handle image uploads with compression and S3 storage.
    """
    image = models.ImageField(
        upload_to='images/', storage=CompressedImageS3Storage())
    module_type = models.CharField(max_length=50, choices=[
                                   ("gallery", "Gallery"), ("banner", "Banner")], null=False)
    status = models.BooleanField(default=True)
    file_size = models.PositiveIntegerField(editable=False, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status:
            print("Status is True, updating other products...", self.pk)
            # Get all other active products of the same module_type
            same_module_products = ImageUpload.objects.filter(
                Q(status=True) &
                ~Q(pk=self.pk)  # Exclude current instance if it exists
            )

            # Set their status to False
            same_module_products.update(status=False)

        # 1) Save the instance (this uploads/compresses the image)
        super().save(*args, **kwargs)

        # 2) Now get the size from the storage backend
        if self.image and hasattr(self.image, 'size'):
            actual_size = self.image.size  # in bytes
        else:
            # fallback: open file from storage to measure
            actual_size = self.image.storage.size(self.image.name)

        # 3) If it’s changed (or not set yet), write it back without looping
        if self.file_size != actual_size:
            self.file_size = actual_size
            super().save(update_fields=['file_size'])

    @property
    def cloudfront_url(self):
        if self.image:
            return f"https://{AWS_CLOUDFRONT_DOMAIN}/{self.image.name}"
        return None

    def __str__(self):
        return f"Image {self.id} - {self.module_type}"
