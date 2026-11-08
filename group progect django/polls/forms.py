from django import forms
from .models import Choice, Poll


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["title", "description", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class AnswerForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Choice.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None,
        label="Оберіть одну відповідь",
    )

    def __init__(self, *args, question, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["choice"].queryset = question.choices.all()
        self.fields["choice"].label = question.text
        if not question.required:
            self.fields["choice"].required = False
