from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Announcement
from .forms import AnnouncementForm


class AdminOrModeratorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return (
            user.is_superuser or
            user.is_staff or
            user.groups.filter(name__in=["Moderators", "Модератори"]).exists()
        )


class AnnouncementListView(ListView):
    model = Announcement
    template_name = "announcements/announcement_list.html"
    context_object_name = "announcements"

    def get_queryset(self):
        now = timezone.now()
        qs = Announcement.objects.filter(
            published_at__lte=now
        ).filter(
            Q(expires_at__isnull=True) | Q(expires_at__gte=now)
        )

        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = "announcements/announcement_detail.html"
    context_object_name = "announcement"


class AnnouncementCreateView(AdminOrModeratorRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcements/announcement_form.html"
    success_url = reverse_lazy("announcement_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AnnouncementUpdateView(AdminOrModeratorRequiredMixin, UpdateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcements/announcement_form.html"
    success_url = reverse_lazy("announcement_list")


class AnnouncementDeleteView(AdminOrModeratorRequiredMixin, DeleteView):
    model = Announcement
    template_name = "announcements/announcement_confirm_delete.html"
    success_url = reverse_lazy("announcement_list")