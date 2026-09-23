from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import MediaFile
from .serializers import MediaFileSerializer
from chat.models import Conversation

class MediaUploadAPIView(APIView):
    def post(self, request):
        uploaded_file = request.FILES.get("file")
        conversation_id = request.data.get("conversation_id")

        if not uploaded_file:
            return Response(
                {"error": "File is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        content_type = uploaded_file.content_type

        if content_type.startswith("image/"):
            media_type = "image"
        elif content_type.startswith("audio/"):
            media_type = "audio"
        elif content_type.startswith("video/"):
            media_type = "video"
        else:
            return Response(
                {"error": "Only image, audio and video are supported."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = None
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                pass

        media = MediaFile.objects.create(
            file=uploaded_file,
            media_type=media_type,
            conversation=conversation,
            description=""
        )

        serializer = MediaFileSerializer(media)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )