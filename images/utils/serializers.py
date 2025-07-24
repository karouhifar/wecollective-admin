# serializers.py
from rest_framework import serializers

from images.models import ImageUpload


class ImageMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['id', 'cloudfront_url', 'module_type',
                  'file_size']
