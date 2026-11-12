from django.urls import path
from . import views

app_name = "forum"

urlpatterns = [
    path("", views.ForumHomeView.as_view(), name="home"),
    path("create/", views.TopicCreateView.as_view(), name="topic_create"),
]
