from . import views
from django.urls import path

app_name = 'tombola'

urlpatterns = [
    path('home/', views.home, name='home'),
]