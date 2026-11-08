from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "user", "Користувач"
        MODERATOR = "moderator", "Модератор"
        ADMINISTRATOR = "administrator", "Адміністратор"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    first_name = models.CharField("Ім'я", max_length=150, blank=True)
    last_name = models.CharField("Прізвище", max_length=150, blank=True)
    email = models.EmailField("Електронна пошта", unique=True)

    class Meta:
        verbose_name = "користувач"
        verbose_name_plural = "користувачі"
        ordering = ["last_name", "first_name", "username"]

    def __str__(self):
        return self.get_full_name() or self.username


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField("Про себе", blank=True)
    avatar = models.ImageField("Аватар", upload_to="profiles/avatars/", blank=True)
    phone = models.CharField("Телефон", max_length=30, blank=True)
    website = models.URLField("Вебсайт", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "профіль користувача"
        verbose_name_plural = "профілі користувачів"

    def __str__(self):
        return f"Профіль: {self.user}"


class GroupInformation(models.Model):
    name = models.CharField("Назва групи", max_length=120)
    description = models.TextField("Інформація про групу", blank=True)
    curator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="curated_groups")
    contact_email = models.EmailField("Контактна пошта", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "інформація про групу"
        verbose_name_plural = "інформація про групу"

    def __str__(self):
        return self.name
