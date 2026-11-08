from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Poll(models.Model):
    title = models.CharField("Назва", max_length=200)
    description = models.TextField("Опис", blank=True)
    is_published = models.BooleanField("Опубліковано", default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="created_polls", verbose_name="Автор"
    )
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Опитування"
        verbose_name_plural = "Опитування"

    def __str__(self):
        return self.title


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="questions", verbose_name="Опитування")
    text = models.CharField("Текст запитання", max_length=500)
    order = models.PositiveIntegerField("Порядок", default=1, validators=[MinValueValidator(1)])
    required = models.BooleanField("Обов'язкове", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Запитання"
        verbose_name_plural = "Запитання"
        constraints = [
            models.UniqueConstraint(fields=["poll", "order"], name="unique_question_order_per_poll")
        ]

    def __str__(self):
        return f"{self.poll.title}: {self.text[:60]}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices", verbose_name="Запитання")
    text = models.CharField("Варіант відповіді", max_length=300)
    order = models.PositiveIntegerField("Порядок", default=1)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Варіант відповіді"
        verbose_name_plural = "Варіанти відповідей"

    def __str__(self):
        return self.text


class PollAttempt(models.Model):
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_IN_PROGRESS, "У процесі"),
        (STATUS_COMPLETED, "Завершено"),
    ]

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="attempts", verbose_name="Опитування")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="poll_attempts", verbose_name="Користувач")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)
    started_at = models.DateTimeField("Початок", auto_now_add=True)
    completed_at = models.DateTimeField("Завершено", null=True, blank=True)

    class Meta:
        ordering = ["-started_at"]
        verbose_name = "Проходження"
        verbose_name_plural = "Проходження"
        constraints = [
            models.UniqueConstraint(fields=["poll", "user"], name="one_current_attempt_per_user_poll")
        ]

    def __str__(self):
        return f"{self.user} — {self.poll} ({self.get_status_display()})"


class Answer(models.Model):
    attempt = models.ForeignKey(PollAttempt, on_delete=models.CASCADE, related_name="answers", verbose_name="Проходження")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name="Запитання")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="answers", verbose_name="Обрана відповідь")

    class Meta:
        verbose_name = "Відповідь"
        verbose_name_plural = "Відповіді"
        constraints = [
            models.UniqueConstraint(fields=["attempt", "question"], name="one_answer_per_question_attempt")
        ]

    def __str__(self):
        return f"{self.question}: {self.choice}"
