
from calendar import monthrange, monthcalendar
from datetime import date, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from .models import Event
from .forms import EventForm


class EventListView(ListView):
    model = Event
    template_name = "events.html"
    context_object_name = "events"


class EventCalendarView(TemplateView):
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()

        try:
            year = int(self.request.GET.get("year", today.year))
            month = int(self.request.GET.get("month", today.month))
            first_day = date(year, month, 1)
        except (ValueError, TypeError):
            first_day = today.replace(day=1)
            year = first_day.year
            month = first_day.month

        events = Event.objects.filter(
            starts_at__year=year,
            starts_at__month=month
        ).order_by("starts_at")

        events_by_day = {}

        for event in events:
            day = event.starts_at.day
            events_by_day.setdefault(day, []).append(event)

        weeks = monthcalendar(year, month)

        calendar_weeks = []

        for week in weeks:
            calendar_week = []

            for day in week:
                calendar_week.append({
                    "day": day,
                    "events": events_by_day.get(day, [])
                })

            calendar_weeks.append(calendar_week)

        previous_month = first_day - timedelta(days=1)

        next_month = (
            first_day.replace(day=monthrange(year, month)[1])
            + timedelta(days=1)
        )

        context["calendar_weeks"] = calendar_weeks
        context["calendar_year"] = year
        context["calendar_month"] = month
        context["previous_month"] = previous_month
        context["next_month"] = next_month

        return context

class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["can_manage_events"] = (
            user.is_authenticated
            and (
                user.is_staff
                or user.is_superuser
                or user.groups.filter(name="Модератори").exists()
            )
        )

        return context


class ModeratorOrAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated
            and (
                user.is_superuser
                or user.is_staff
                or user.groups.filter(name="Модератори").exists()
            )
        )


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "event_form.html"
    success_url = reverse_lazy("event_list")
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EventUpdateView(ModeratorOrAdminMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "event_form.html"
    success_url = reverse_lazy("event_list")


class EventDeleteView(ModeratorOrAdminMixin, DeleteView):
    model = Event
    template_name = "event_confirm_delete.html"
    success_url = reverse_lazy("event_list")
