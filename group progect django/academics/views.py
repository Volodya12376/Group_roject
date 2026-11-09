from django.shortcuts import render
from django.views.generic import ListView
from app.models import Marks
from django.contrib.auth.models import User

class MarksListView(ListView):
    model = Marks
    template_name = "marks_list.html"
    context_object_name = "marks"

    def get_queryset(self):
        return Marks.objects.filter(
            student_id=self.kwargs["student_id"]
        ).select_related("lesson", "student").order_by("-lesson_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Оцінки учня"
        context["student"] = User.objects.get(
            id=self.kwargs["student_id"]
        )

        return context

class StudentsListView(ListView):
    model = Marks
    template_name = "students_with_marks.html"
    context_object_name = "students"

    def get_queryset(self):
        return User.objects.filter(
            id__in=Marks.objects.values_list("student_id", flat=True)
        ).distinct()