from django.conf import settings
from django.db import models


class PortfolioProject(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolio_projects")
    title = models.CharField("Назва проєкту", max_length=200)
    description = models.TextField("Опис", blank=True)
    project_url = models.URLField("Посилання на проєкт", blank=True)
    repository_url = models.URLField("Посилання на репозиторій", blank=True)
    preview_image = models.ImageField("Зображення проєкту", upload_to="portfolio/previews/", blank=True)
    attachment = models.FileField("Файл проєкту", upload_to="portfolio/files/", blank=True)
    is_public = models.BooleanField("Публічний проєкт", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "проєкт портфоліо"
        verbose_name_plural = "проєкти портфоліо"

    def __str__(self):
        return f"{self.title} — {self.owner}"
