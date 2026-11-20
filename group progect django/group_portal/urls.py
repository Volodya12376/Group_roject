
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("events.urls")),
    path("academics/", include("academics.urls")),
    path("accounts/", include("accounts.urls")),
    path("forum/", include("forum.urls")),
    path("announcements/", include("announcements.urls")),
    path("materials/", include("materials.urls")),
    path("polls/", include("polls.urls")),
    path("portfolio/", include("portfolio.urls")),
    path("voting/", include("voting.urls")),
]
