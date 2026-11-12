from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Topic


class ForumHomeView(ListView):
    model = Topic
    template_name = "forum/topic_list.html"
    context_object_name = "topics"


class TopicCreateView(CreateView):
    model = Topic
    fields = ["title", "content"]
    template_name = "forum/topic_form.html"
    success_url = reverse_lazy("forum:home")

