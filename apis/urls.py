from django.urls import path
from . import views

app_name = 'apis'

urlpatterns = [
    path('category/', views.category_api, name='category_api'),
    path('category/<slug>/', views.category_api, name='by_category_api'),

    path('product/', views.product_api, name='product_api'),
    path('variation/', views.variation_api, name='variation_api'),
    
    path('color/', views.color_api, name='color_api'),
    path('color/<slug>/', views.color_api, name='by_color_api'),

    path('register/', views.Registrationuser_api, name='register_api'),
    path('activate/<uidb64>/<token>/', views.Activate_api, name="activation_email_api"),

    path('logout/', views.logout, name='logout'),

]