from rest_framework import serializers
from .models import Diagnosis
from chat.models import Conversation


class DiagnosisSerializer(serializers.ModelSerializer):
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(),
        source='conversation'
    )

    class Meta:
        model = Diagnosis

        fields = [
            "id",
            "conversation_id",
            "problem",
            "diagnosis",
            "recommendation",
            "severity",
            "created_at"
        ]