from .views import MarksListView, StudentsListView
from django.urls import path

urlpatterns = [
    path('marks/', MarksListView.as_view(), name='marks'),
    path('students_with_marks/', StudentsListView.as_view(), name='students'),
    path(
        "students_with_marks/<int:student_id>/",
        MarksListView.as_view(),
        name="student_marks"
    )
]