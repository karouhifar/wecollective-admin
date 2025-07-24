from django.urls import path
from . import views


urlpatterns = [
    path('bg-images/', views.get_background_image, name='background-image'),
]
