from . import views
from django.urls import path

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('order_payment/<order_id>/', views.order_payment, name='order_payment'),
    path('admin/pdf/<int:order_id>/', views.admin_order_pdf, name='admin_order_pdf'),

    #stripe
    path('create_stripe_session/<order_id>/', views.create_stripe_session, name="create_stripe_session"),
    path('payment_success/', views.payment_success, name="payment_stripe_success"),
    path('payment_failed/' , views.payment_failed , name="payment_stripe_failed"),
    path('stripe/webhook/' , views.stripe_webhook , name="stripe_webhook"),

    path('history/', views.orders_history, name='orders_history'),
    path('history/order/<order_id>/', views.order_detail, name="order_detail"),

]