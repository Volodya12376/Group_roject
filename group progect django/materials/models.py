from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Material(models.Model):
    class MaterialType(models.TextChoices):
        FILE = "file", "Файл"
        IMAGE = "image", "Зображення"
        LINK = "link", "Посилання"
        YOUTUBE = "youtube", "YouTube-відео"

    title = models.CharField("Назва матеріалу", max_length=200)
    description = models.TextField("Опис", blank=True)
    material_type = models.CharField(max_length=10, choices=MaterialType.choices)
    file = models.FileField("Файл", upload_to="materials/files/", blank=True)
    image = models.ImageField("Зображення", upload_to="materials/images/", blank=True)
    url = models.URLField("Посилання", blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="materials_uploaded")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "навчальний матеріал"
        verbose_name_plural = "навчальні матеріали"

    def clean(self):
        if self.material_type == self.MaterialType.FILE and not self.file:
            raise ValidationError({"file": "Для типу «Файл» потрібно додати файл."})
        if self.material_type == self.MaterialType.IMAGE and not self.image:
            raise ValidationError({"image": "Для типу «Зображення» потрібно додати зображення."})
        if self.material_type in (self.MaterialType.LINK, self.MaterialType.YOUTUBE) and not self.url:
            raise ValidationError({"url": "Для цього типу матеріалу потрібно вказати посилання."})

    def __str__(self):
        return self.title
