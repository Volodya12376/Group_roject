from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Subject(models.Model):

    name = models.CharField("Назва предмета", max_length=120, unique=True)
    description = models.TextField("Опис", blank=True)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teaching_subjects",
        verbose_name="Викладач",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "навчальний предмет"
        verbose_name_plural = "навчальні предмети"

    def __str__(self):
        return self.name


class Grade(models.Model):

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="grades_received",
        verbose_name="Учень",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="grades",
        verbose_name="Предмет",
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="grades_given",
        verbose_name="Викладач",
    )
    value = models.PositiveSmallIntegerField(
        "Оцінка",
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    date = models.DateField("Дата оцінювання")
    topic = models.CharField("Тема / вид роботи", max_length=200, blank=True)
    comment = models.TextField("Коментар", blank=True)
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        ordering = ["-date", "subject__name"]
        indexes = [
            models.Index(fields=["student", "date"]),
            models.Index(fields=["subject", "date"]),
        ]
        verbose_name = "оцінка"
        verbose_name_plural = "оцінки"

    def __str__(self):
        return f"{self.student} — {self.subject}: {self.value} ({self.date})"
