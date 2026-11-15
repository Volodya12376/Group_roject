from django import forms
from .models import PortfolioProject


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = [
            "title",
            "description",
            "project_url",
            "repository_url",
            "preview_image",
            "attachment",
            "is_public",
        ]