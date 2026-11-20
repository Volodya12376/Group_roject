
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import PortfolioProject
from .forms import PortfolioForm


def portfolio_list(request):
    portfolios = PortfolioProject.objects.select_related("owner")

    # Показуємо публічні проєкти всім,
    # а приватні — тільки їхнім власникам.
    if request.user.is_authenticated:
        portfolios = portfolios.filter(
            Q(is_public=True) | Q(owner=request.user)
        )
    else:
        portfolios = portfolios.filter(is_public=True)

    return render(request, "portfolio/list.html", {
        "portfolios": portfolios
    })


@login_required
def portfolio_create(request):
    form = PortfolioForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():
        portfolio = form.save(commit=False)
        portfolio.owner = request.user
        portfolio.save()
        return redirect("portfolio_list")

    return render(request, "portfolio/form.html", {
        "form": form,
        "title": "Додати проєкт"
    })


@login_required
def portfolio_edit(request, pk):
    portfolio = get_object_or_404(
        PortfolioProject,
        pk=pk,
        owner=request.user
    )

    form = PortfolioForm(
        request.POST or None,
        request.FILES or None,
        instance=portfolio
    )

    if form.is_valid():
        form.save()
        return redirect("portfolio_list")

    return render(request, "portfolio/form.html", {
        "form": form,
        "title": "Редагувати проєкт"
    })


@login_required
def portfolio_delete(request, pk):
    portfolio = get_object_or_404(
        PortfolioProject,
        pk=pk,
        owner=request.user
    )

    if request.method == "POST":
        portfolio.delete()
        return redirect("portfolio_list")

    return render(request, "portfolio/delete.html", {
        "portfolio": portfolio
    })
