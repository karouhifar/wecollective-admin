
from django.db import models
from images.utils.compress import CompressedImageS3Storage
# Create your models here.


class ImageUpload(models.Model):
    image = models.ImageField(
        upload_to='images/', storage=CompressedImageS3Storage())
    module_type = models.CharField(max_length=50, choices=[
                                   ("gallery", "Gallery"), ("banner", "Banner")], null=False)
    status = models.BooleanField(default=True)
    file_size = models.PositiveIntegerField(editable=False, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} - {self.module_type}"
