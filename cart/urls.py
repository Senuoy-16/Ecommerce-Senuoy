from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:variation_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_from_form/<int:variation_id>/', views.add_from_form, name='add_from_form'),
    path('remove/<int:variation_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('', views.cart_detail, name='cart_detail'),
]