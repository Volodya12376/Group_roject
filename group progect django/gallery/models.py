from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class GalleryItem(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Фото"
        VIDEO = "video", "Відео"

    class ModerationStatus(models.TextChoices):
        PENDING = "pending", "Очікує перевірки"
        APPROVED = "approved", "Схвалено"
        REJECTED = "rejected", "Відхилено"

    title = models.CharField("Назва", max_length=200, blank=True)
    description = models.TextField("Опис", blank=True)
    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    image = models.ImageField("Фото", upload_to="gallery/images/", blank=True)
    video_file = models.FileField("Відеофайл", upload_to="gallery/videos/", blank=True)
    video_url = models.URLField("Посилання на відео", blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="gallery_items")
    moderation_status = models.CharField(max_length=10, choices=ModerationStatus.choices, default=ModerationStatus.PENDING)
    moderated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="gallery_items_moderated")
    moderation_comment = models.TextField("Коментар модератора", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    moderated_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.media_type == self.MediaType.IMAGE and not self.image:
            raise ValidationError({"image": "Для фото потрібно додати файл зображення."})
        if self.media_type == self.MediaType.VIDEO and not (self.video_file or self.video_url):
            raise ValidationError({"video_file": "Для відео потрібно додати файл або посилання."})

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "елемент галереї"
        verbose_name_plural = "галерея"

    def __str__(self):
        return self.title or f"{self.get_media_type_display()} — {self.uploaded_by}"
