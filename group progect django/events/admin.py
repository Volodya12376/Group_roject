from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "starts_at", "ends_at", "created_by")
    search_fields = ("title", "description")
    list_filter = ("starts_at",)