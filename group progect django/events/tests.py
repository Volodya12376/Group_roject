
from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from .models import Event


class EventTests(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
            title="Подія",
            description="Опис події",
            location="Київ",
            starts_at=timezone.make_aware(
                datetime(2030, 1, 1, 10, 0)
            ),
    )

    def test_event_title(self):
        self.assertEqual(self.event.title, "Подія")

    def test_event_location(self):
        self.assertEqual(self.event.location, "Київ")

    def test_event_exists(self):
        self.assertTrue(
            Event.objects.filter(title=self.event.title).exists()
    )

    def test_event_list_page(self):
        response = self.client.get(reverse("event_list"))
        self.assertEqual(response.status_code, 200)

    def test_event_detail_page(self):
        response = self.client.get(
            reverse("event_detail", args=[self.event.pk])
        )
        self.assertEqual(response.status_code, 200)
