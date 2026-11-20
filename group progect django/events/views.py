from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Event
from .forms import EventForm


class EventListView(ListView):
    model = Event
    template_name = "events.html"
    context_object_name = "events"
    ordering = ["starts_at"]


class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"
    context_object_name = "event"


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
        return (
            self.request.user.is_staff
            or self.request.user.groups.filter(name__in=["admin", "moderator", "Адміністратор", "Модератор"]).exists()
        )


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    template_name = "event_confirm_delete.html"
    success_url = reverse_lazy("events:events")

    def test_func(self):
        return (
            self.request.user.is_staff
            or self.request.user.groups.filter(name__in=["admin", "moderator", "Адміністратор", "Модератор"]).exists()
        )


class EventCalendarView(ListView):
    model = Event
    template_name = "calendar.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.all().order_by("starts_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()

        context["calendar_month"] = now.month
        context["calendar_year"] = now.year

        return context