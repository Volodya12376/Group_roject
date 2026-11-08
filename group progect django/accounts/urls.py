from django.urls import path
from .views import login_view, register_view, start_page_view 

urlpatterns = [
    path('', start_page_view, name='start_page'), 
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]