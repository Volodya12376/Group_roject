from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


class ForumCategory(models.Model):
    title = models.CharField("Назва розділу", max_length=120, unique=True)
    description = models.TextField("Опис", blank=True)
    position = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="forum_categories_created")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "title"]
        verbose_name = "розділ форуму"
        verbose_name_plural = "розділи форуму"

    def __str__(self):
        return self.title


class ForumTopic(models.Model):
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField("Тема", max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField("Опис теми", blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forum_topics")
    is_pinned = models.BooleanField("Закріплена", default=False)
    is_closed = models.BooleanField("Закрита для відповідей", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_pinned", "-updated_at"]
        verbose_name = "тема форуму"
        verbose_name_plural = "теми форуму"

    def __str__(self):
        return self.title


class ForumPost(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forum_posts")
    content = models.TextField("Повідомлення", validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "повідомлення форуму"
        verbose_name_plural = "повідомлення форуму"

    def __str__(self):
        return f"{self.author}: {self.content[:50]}"
