from django.urls import path
from .views import MarksListView, StudentsListView

urlpatterns = [
    path("marks/", StudentsListView.as_view(), name="marks"),
    path(
        "students_with_marks/",
        StudentsListView.as_view(),
        name="students"
    ),
    path(
        "students_with_marks/<int:student_id>/",
        MarksListView.as_view(),
        name="student_marks"
    ),
]