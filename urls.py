"""
URL configuration for events project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.EventListView.as_view(), name="event_list"),
    path("calendar/", views.EventCalendarView.as_view(), name="event_calendar"),
    path("<int:pk>/", views.EventDetailView.as_view(), name="event_detail"),
    path("create/", views.EventCreateView.as_view(), name="event_create"),
    path("<int:pk>/edit/", views.EventUpdateView.as_view(), name="event_update"),
    path("<int:pk>/delete/", views.EventDeleteView.as_view(), name="event_delete"),
]
