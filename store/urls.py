from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [ 
    path('', views.home, name='home'),
    path('list_product/', views.list_product, name='list_product'),
    path('product/<variation_id>/', views.product_detail, name='product_detail'),
    path('category/<category_slug>/', views.product_by_category, name='product_by_category'),
]