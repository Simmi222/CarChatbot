from django.urls import path
from .views import MediaUploadAPIView


urlpatterns = [
    path("", MediaUploadAPIView.as_view()),
]