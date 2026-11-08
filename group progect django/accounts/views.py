from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views.generic import TemplateView


def start_page_view(request):
    user = request.user
    role = "Гость"
    
    if user.is_authenticated:
        if user.is_superuser:
            role = "Адміністратор"
        elif user.groups.filter(name='Moderators').exists() or user.is_staff:
            role = "Модератор"
        else:
            role = "Звичайний користувач"
            
    return render(request, 'authentif/start_page.html', {'role': role})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('start_page')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('start_page')  
    else:
        form = AuthenticationForm()
    
    return render(request, 'authentif/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('start_page')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)  
            return redirect('start_page')  
    else:
        form = UserCreationForm()
    
    return render(request, 'authentif/register.html', {'form': form})