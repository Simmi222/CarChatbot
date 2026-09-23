from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking

        fields = [
            "id",
            "customer_name",
            "phone",
            "vehicle",
            "problem",
            "preferred_date",
            "preferred_time",
            "status",
            "created_at"
        ]

        read_only_fields = [
            "id",
            "status",
            "created_at"
        ]