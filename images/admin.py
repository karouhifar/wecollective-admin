from django.contrib import admin
from .models import ImageUpload


@admin.register(ImageUpload)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ["id", "module_type", "status", "uploaded_at", "image"]
    list_filter = ["module_type", "status"]
    list_editable = ["status"]
    readonly_fields = ["file_size"]  # file_size will be set automatically
    list_per_page = 10
