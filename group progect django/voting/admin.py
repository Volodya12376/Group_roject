
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from .models import Poll, PollOption, PollVote


class PollOptionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        # Призначаємо номери варіантам до перевірки унікальності.
        order = 1

        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue

            if not form.cleaned_data or form.cleaned_data.get("DELETE"):
                continue

            form.cleaned_data["order"] = order
            form.instance.order = order
            order += 1

        super().clean()


class PollOptionInline(admin.TabularInline):
    model = PollOption
    formset = PollOptionInlineFormSet
    fields = ("text", "order")
    extra = 2


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_by", "created_at")
    list_filter = ("is_active", "show_results")
    search_fields = ("title", "description")
    inlines = [PollOptionInline]

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ("poll", "user", "option", "created_at")
    list_filter = ("poll", "created_at")


admin.site.register(PollOption)
