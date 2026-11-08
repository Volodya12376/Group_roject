from django.conf import settings
from django.db import models


class Announcement(models.Model):
    title = models.CharField("Заголовок оголошення", max_length=200)
    content = models.TextField("Текст оголошення")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="announcements")
    is_pinned = models.BooleanField("Закріплене", default=False)
    published_at = models.DateTimeField("Дата публікації", null=True, blank=True)
    expires_at = models.DateTimeField("Дата завершення", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_pinned", "-published_at", "-created_at"]
        verbose_name = "оголошення"
        verbose_name_plural = "оголошення"

    def __str__(self):
        return self.title
