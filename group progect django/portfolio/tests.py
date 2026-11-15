from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Portfolio


class PortfolioTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="12345"
        )

        self.portfolio = Portfolio.objects.create(
            user=self.user,
            title="Мій перший проєкт",
            description="Тестовий опис проєкту"
        )

    # Тест перегляду портфоліо
    def test_portfolio_list(self):
        response = self.client.get(reverse("portfolio_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Мій перший проєкт")

    # Тест додавання проєкту
    def test_portfolio_create(self):
        self.client.login(
            username="testuser",
            password="12345"
        )

        response = self.client.post(
            reverse("portfolio_create"),
            {
                "title": "Новий проєкт",
                "description": "Опис нового проєкту",
                "link": ""
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Portfolio.objects.filter(title="Новий проєкт").exists()
        )

    # Тест редагування проєкту
    def test_portfolio_edit(self):
        self.client.login(
            username="testuser",
            password="12345"
        )

        response = self.client.post(
            reverse("portfolio_edit", args=[self.portfolio.pk]),
            {
                "title": "Оновлений проєкт",
                "description": "Новий опис",
                "link": ""
            }
        )

        self.assertEqual(response.status_code, 302)

        self.portfolio.refresh_from_db()

        self.assertEqual(
            self.portfolio.title,
            "Оновлений проєкт"
        )

    # Тест видалення проєкту
    def test_portfolio_delete(self):
        self.client.login(
            username="testuser",
            password="12345"
        )

        response = self.client.post(
            reverse("portfolio_delete", args=[self.portfolio.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Portfolio.objects.filter(pk=self.portfolio.pk).exists()
        )
