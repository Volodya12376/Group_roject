from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class Event(models.Model):
    title = models.CharField("Назва події", max_length=200)
    description = models.TextField("Опис", blank=True)
    location = models.CharField("Місце проведення", max_length=255, blank=True)
    starts_at = models.DateTimeField("Початок")
    ends_at = models.DateTimeField("Завершення", null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="events_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["starts_at"]
        verbose_name = "подія"
        verbose_name_plural = "події"

    def clean(self):
        if self.ends_at and self.ends_at < self.starts_at:
            raise ValidationError({"ends_at": "Час завершення не може бути раніше часу початку."})

    def __str__(self):
        return self.title
