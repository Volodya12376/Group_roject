
from django.urls import path
from . import views

urlpatterns = [
    path("", views.poll_list, name="poll_list"),
    path("add/", views.add_poll, name="add_poll"),
    path("delete/<int:poll_id>/", views.delete_poll, name="delete_poll"),
    path("poll/<int:poll_id>/", views.poll_detail, name="poll_detail"),
    path("poll/<int:poll_id>/vote/", views.VoteView.as_view(), name="vote"),
    path("poll/<int:poll_id>/results/", views.results, name="results"),
]
