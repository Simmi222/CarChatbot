from django.urls import path
from .views import DiagnosisAPIView


urlpatterns = [
    path("", DiagnosisAPIView.as_view()),
]