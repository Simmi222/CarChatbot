from rest_framework import serializers
from .models import MediaFile
from chat.models import Conversation


class MediaFileSerializer(serializers.ModelSerializer):
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(),
        source='conversation',
        required=False,
        allow_null=True
    )

    class Meta:
        model = MediaFile

        fields = [
            "id",
            "conversation_id",
            "file",
            "media_type",
            "description",
            "uploaded_at"
        ]