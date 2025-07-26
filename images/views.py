# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from images.models import ImageUpload
from images.utils.serializers import ImageMetadataSerializer


@api_view(['GET'])
def get_background_image(request):
    background_image = ImageUpload.objects.filter(status=True).first()
    if not background_image:
        return Response(
            {"message": "No background image found"},
            status=404
        )

    serializer = ImageMetadataSerializer(background_image)
    return Response(serializer.data)
