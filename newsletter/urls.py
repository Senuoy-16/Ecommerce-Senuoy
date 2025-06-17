from django.urls import path
from .views import subscribe_newsletter

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
]