from django.urls import path

from .views import (
    EventListView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    EventCalendarView,
)

app_name = "events"

urlpatterns = [
    path("", EventListView.as_view(), name="events"),
    path("calendar/", EventCalendarView.as_view(), name="event_calendar"),
    path("create/", EventCreateView.as_view(), name="event_create"),
    path("<int:pk>/", EventDetailView.as_view(), name="event_detail"),
    path("<int:pk>/edit/", EventUpdateView.as_view(), name="event_update"),
    path("<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
]