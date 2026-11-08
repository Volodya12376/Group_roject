from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Poll(models.Model):
    title = models.CharField("Назва голосування", max_length=200)
    description = models.TextField("Опис", blank=True)
    is_active = models.BooleanField(default=True)
    allow_revote = models.BooleanField("Дозволити переголосування", default=True)
    show_results = models.BooleanField("Показувати результати всім", default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="polls_created")
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "голосування"
        verbose_name_plural = "голосування"

    def clean(self):
        if self.starts_at and self.ends_at and self.ends_at < self.starts_at:
            raise ValidationError({"ends_at": "Завершення голосування не може бути раніше початку."})

    def __str__(self):
        return self.title


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    text = models.CharField("Варіант голосування", max_length=300)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]
        constraints = [models.UniqueConstraint(fields=["poll", "order"], name="unique_poll_option_order")]
        verbose_name = "варіант голосування"
        verbose_name_plural = "варіанти голосування"

    def __str__(self):
        return self.text


class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="poll_votes")
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["poll", "user"], name="unique_poll_vote_per_user")]
        verbose_name = "голос"
        verbose_name_plural = "голоси"

    def clean(self):
        if self.option_id and self.poll_id and self.option.poll_id != self.poll_id:
            raise ValidationError({"option": "Обраний варіант має належати цьому голосуванню."})

    def __str__(self):
        return f"{self.user} — {self.poll}: {self.option}"
