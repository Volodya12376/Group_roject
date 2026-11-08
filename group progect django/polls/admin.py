from django.contrib import admin
from .models import Poll, Question, Choice, PollAttempt, Answer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_by", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description")
    inlines = [QuestionInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "poll", "order", "required")
    list_filter = ("poll", "required")
    search_fields = ("text", "poll__title")
    inlines = [ChoiceInline]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ("question", "choice")
    can_delete = False


@admin.register(PollAttempt)
class PollAttemptAdmin(admin.ModelAdmin):
    list_display = ("poll", "user", "status", "started_at", "completed_at")
    list_filter = ("poll", "status", "completed_at")
    search_fields = ("poll__title", "user__username", "user__email")
    inlines = [AnswerInline]
    readonly_fields = ("poll", "user", "status", "started_at", "completed_at")
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name="Moderator").exists() or request.user.has_perm("polls.view_pollattempt")
