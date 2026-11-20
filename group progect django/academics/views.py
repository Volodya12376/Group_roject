from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from .models import Marks

User = get_user_model()


class MarksListView(ListView):
    model = Marks
    template_name = "marks_list.html"
    context_object_name = "marks"

    def get_queryset(self):
        return Marks.objects.filter(
            student_id=self.kwargs["student_id"]
        ).select_related(
            "lesson", "student"
        ).order_by("-lesson_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Оцінки учня"
        context["student"] = get_object_or_404(
            User,
            pk=self.kwargs["student_id"]
        )

        return context


class StudentsListView(ListView):
    model = Marks
    template_name = "students_with_marks.html"
    context_object_name = "students"

    def get_queryset(self):
        return User.objects.filter(
            pk__in=Marks.objects.values_list(
                "student_id",
                flat=True
            )
        ).distinct().order_by(
            "last_name",
            "first_name",
            "username"
        )