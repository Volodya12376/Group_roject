
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .models import ForumTopic


class ForumHomeView(ListView):
    model = ForumTopic
    template_name = "forum/topic_list.html"
    context_object_name = "topics"

    def get_queryset(self):
        return ForumTopic.objects.select_related(
            "category",
            "created_by"
        ).order_by("-is_pinned", "-updated_at")


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = ForumTopic
    fields = ["category", "title", "description"]
    template_name = "forum/topic_form.html"
    success_url = reverse_lazy("forum:home")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
