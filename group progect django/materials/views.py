from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Material
from .forms import MaterialForm


class AdminOrModeratorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return (
            user.is_superuser or
            user.is_staff or
            user.groups.filter(name__in=["Moderators", "Модератори"]).exists()
        )


class MaterialListView(ListView):
    model = Material
    template_name = "materials/material_list.html"
    context_object_name = "materials"

    def get_queryset(self):
        qs = Material.objects.filter(is_published=True)

        q = self.request.GET.get("q", "").strip()
        material_type = self.request.GET.get("type", "").strip()

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if material_type in dict(Material.MaterialType.choices):
            qs = qs.filter(material_type=material_type)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["selected_type"] = self.request.GET.get("type", "")
        context["material_types"] = Material.MaterialType.choices
        return context


class MaterialDetailView(DetailView):
    model = Material
    template_name = "materials/material_detail.html"
    context_object_name = "material"


class MaterialCreateView(AdminOrModeratorRequiredMixin, CreateView):
    model = Material
    form_class = MaterialForm
    template_name = "materials/material_form.html"
    success_url = reverse_lazy("material_list")

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)


class MaterialUpdateView(AdminOrModeratorRequiredMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = "materials/material_form.html"
    success_url = reverse_lazy("material_list")


class MaterialDeleteView(AdminOrModeratorRequiredMixin, DeleteView):
    model = Material
    template_name = "materials/material_confirm_delete.html"
    success_url = reverse_lazy("material_list")
