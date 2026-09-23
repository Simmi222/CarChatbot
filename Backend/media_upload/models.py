from django.db import models

class MediaFile(models.Model):

    MEDIA_TYPES = (
        ("image", "Image"),
        ("audio", "Audio"),
        ("video", "Video"),
    )

    conversation = models.ForeignKey(
        'chat.Conversation',
        on_delete=models.CASCADE,
        related_name='media_files',
        null=True,
        blank=True
    )

    file = models.FileField(upload_to="uploads/")

    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES
    )

    description = models.TextField(blank=True, default='')

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.file.name