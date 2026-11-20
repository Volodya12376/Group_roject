from calendar import Calendar
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Event
from .forms import EventForm


def can_manage_events(user):
    return (
        user.is_authenticated
        and (
            user.is_staff
            or user.is_superuser
            or user.groups.filter(
                name__in=[
                    "admin",
                    "moderator",
                    "Адміністратор",
                    "Модератор",
                    "Moderators",
                    "Модератори",
                ]
            ).exists()
        )
    )


class EventListView(ListView):
    model = Event
    template_name = "events.html"
    context_object_name = "events"
    ordering = ["starts_at"]


class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_manage_events"] = can_manage_events(
            self.request.user
        )
        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_form.html"
    success_url = reverse_lazy("events:events")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event_form.html"
    success_url = reverse_lazy("events:events")

    def test_func(self):
        return can_manage_events(self.request.user)


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = "event_confirm_delete.html"
    success_url = reverse_lazy("events:events")

    def test_func(self):
        return can_manage_events(self.request.user)


class EventCalendarView(ListView):
    model = Event
    template_name = "calendar.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.order_by("starts_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.localdate()

        try:
            year = int(self.request.GET.get("year", today.year))
            month = int(self.request.GET.get("month", today.month))

            if month < 1 or month > 12:
                raise ValueError

            selected_date = date(year, month, 1)

        except (ValueError, TypeError):
            selected_date = date(today.year, today.month, 1)

        year = selected_date.year
        month = selected_date.month

        # Попередній і наступний місяці
        previous_month = (
            date(year - 1, 12, 1)
            if month == 1
            else date(year, month - 1, 1)
        )

        next_month = (
            date(year + 1, 1, 1)
            if month == 12
            else date(year, month + 1, 1)
        )

        # Події вибраного місяця
        month_events = Event.objects.filter(
            starts_at__year=year,
            starts_at__month=month,
        ).order_by("starts_at")

        events_by_day = {}

        for event in month_events:
            day_number = event.starts_at.day
            events_by_day.setdefault(day_number, []).append(event)

        # Формуємо календар з понеділка
        calendar_obj = Calendar(firstweekday=0)
        calendar_weeks = []

        for week in calendar_obj.monthdayscalendar(year, month):
            week_data = []

            for day_number in week:
                week_data.append({
                    "day": day_number,
                    "events": events_by_day.get(day_number, [])
                })

            calendar_weeks.append(week_data)

        context["calendar_month"] = month
        context["calendar_year"] = year
        context["calendar_weeks"] = calendar_weeks
        context["previous_month"] = previous_month
        context["next_month"] = next_month

        return context