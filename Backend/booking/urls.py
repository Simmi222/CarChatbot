from django.urls import path

from .views import (
    BookingAPIView,
    BookingDetailAPIView
)


urlpatterns = [

    path(
        "",
        BookingAPIView.as_view()
    ),

    path(
        "<int:pk>/",
        BookingDetailAPIView.as_view()
    ),
]