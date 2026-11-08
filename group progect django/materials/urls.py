from django.urls import path
from . import views

urlpatterns = [
    path("", views.MaterialListView.as_view(), name="material_list"),
    path("<int:pk>/", views.MaterialDetailView.as_view(), name="material_detail"),
    path("create/", views.MaterialCreateView.as_view(), name="material_create"),
    path("<int:pk>/edit/", views.MaterialUpdateView.as_view(), name="material_update"),
    path("<int:pk>/delete/", views.MaterialDeleteView.as_view(), name="material_delete"),
]