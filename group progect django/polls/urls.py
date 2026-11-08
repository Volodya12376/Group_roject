from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.PollListView.as_view(), name="poll-list"),
    path("manage/", views.PollManageListView.as_view(), name="manage-list"),
    path("manage/create/", views.PollCreateView.as_view(), name="poll-create"),
    path("manage/<int:pk>/edit/", views.PollUpdateView.as_view(), name="poll-update"),
    path("manage/<int:pk>/delete/", views.PollDeleteView.as_view(), name="poll-delete"),
    path("manage/results/", views.ManageResultsView.as_view(), name="manage-results"),
    path("manage/results/<int:pk>/", views.ManageAttemptDetailView.as_view(), name="result-detail"),
    path("<int:pk>/", views.PollDetailView.as_view(), name="poll-detail"),
    path("<int:poll_id>/step/<int:step>/", views.PollStepView.as_view(), name="poll-step"),
    path("<int:pk>/result/", views.MyPollResultView.as_view(), name="my-result"),
    path("<int:pk>/retake/", views.RetakePollView.as_view(), name="retake"),
]
