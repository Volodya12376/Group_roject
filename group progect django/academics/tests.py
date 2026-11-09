from django.test import TestCase
from django.contrib.auth.models import User
from .models import Urok, Marks
from datetime import date


class MarksModelTest(TestCase):

    def setUp(self):
        self.student = User.objects.create_user(
            username="student174",
            password="12345"
        )

        self.lesson = Urok.objects.create(
            name="Ukrainian"
        )

        self.mark = Marks.objects.create(
            lesson=self.lesson,
            student=self.student,
            mark=5,
            lesson_date=date(2026, 11, 1)
        )

    def test_mark_creation(self):
        self.assertEqual(self.mark.mark, 5)
        self.assertEqual(self.mark.lesson.name, "Ukrainian")
        self.assertEqual(self.mark.student.username, "student174")

    def test_mark_count(self):
        self.assertEqual(Marks.objects.count(), 1)

    def test_lesson_date(self):
        self.assertEqual(
            self.mark.lesson_date,
            date(2026, 11, 1)
        )
