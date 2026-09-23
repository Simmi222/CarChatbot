from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Booking
from .serializers import BookingSerializer


class BookingAPIView(APIView):

    def post(self, request):

        serializer = BookingSerializer(
            data=request.data
        )

        if serializer.is_valid():

            booking = serializer.save()

            return Response(
                BookingSerializer(booking).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BookingDetailAPIView(APIView):

    def get(self, request, pk):

        try:

            booking = Booking.objects.get(
                pk=pk
            )

        except Booking.DoesNotExist:

            return Response(
                {"error": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookingSerializer(booking)

        return Response(serializer.data)