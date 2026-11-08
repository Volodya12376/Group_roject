from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Survey(models.Model):
    title = models.CharField("Назва опитування", max_length=200)
    description = models.TextField("Опис", blank=True)
    is_active = models.BooleanField(default=True)
    allow_retake = models.BooleanField("Дозволити повторне проходження", default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="surveys_created")
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "опитування"
        verbose_name_plural = "опитування"

    def clean(self):
        if self.starts_at and self.ends_at and self.ends_at < self.starts_at:
            raise ValidationError({"ends_at": "Завершення опитування не може бути раніше початку."})

    def __str__(self):
        return self.title


class SurveyPage(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="pages")
    title = models.CharField("Назва сторінки", max_length=150, blank=True)
    order = models.PositiveIntegerField("Порядок сторінки", validators=[MinValueValidator(1)])

    class Meta:
        ordering = ["order"]
        constraints = [models.UniqueConstraint(fields=["survey", "order"], name="unique_survey_page_order")]
        verbose_name = "сторінка опитування"
        verbose_name_plural = "сторінки опитування"

    def __str__(self):
        return f"{self.survey} — сторінка {self.order}"


class SurveyQuestion(models.Model):
    class QuestionType(models.TextChoices):
        SINGLE = "single", "Одна відповідь"
        MULTIPLE = "multiple", "Кілька відповідей"
        TEXT = "text", "Текстова відповідь"
        NUMBER = "number", "Числова відповідь"

    page = models.ForeignKey(SurveyPage, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField("Текст запитання")
    question_type = models.CharField(max_length=12, choices=QuestionType.choices, default=QuestionType.SINGLE)
    is_required = models.BooleanField("Обов'язкове", default=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]
        constraints = [models.UniqueConstraint(fields=["page", "order"], name="unique_survey_question_order")]
        verbose_name = "запитання опитування"
        verbose_name_plural = "запитання опитування"

    def __str__(self):
        return self.text[:80]


class SurveyOption(models.Model):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name="options")
    text = models.CharField("Варіант відповіді", max_length=300)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]
        constraints = [models.UniqueConstraint(fields=["question", "order"], name="unique_survey_option_order")]
        verbose_name = "варіант відповіді"
        verbose_name_plural = "варіанти відповідей"

    def __str__(self):
        return self.text


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="survey_responses")
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["survey", "user"], name="unique_survey_response_per_user")]
        ordering = ["-updated_at"]
        verbose_name = "відповідь на опитування"
        verbose_name_plural = "відповіді на опитування"

    def __str__(self):
        return f"{self.user} — {self.survey}"


class SurveyAnswer(models.Model):
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name="answers")
    selected_options = models.ManyToManyField(SurveyOption, blank=True, related_name="answers")
    text_answer = models.TextField("Текстова відповідь", blank=True)
    number_answer = models.DecimalField("Числова відповідь", max_digits=12, decimal_places=2, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["response", "question"], name="unique_answer_per_question")]
        verbose_name = "відповідь на запитання"
        verbose_name_plural = "відповіді на запитання"

    def clean(self):
        if self.question_id and self.response_id:
            if self.question.page.survey_id != self.response.survey_id:
                raise ValidationError("Запитання має належати тому самому опитуванню, що й відповідь.")

    def __str__(self):
        return f"Відповідь: {self.question}"
