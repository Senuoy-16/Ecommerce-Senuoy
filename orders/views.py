from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import OrderItem, Order
from coupons.models import Coupon
from .forms import OrderCreateForm
from cart.cart import Cart
from django.conf import settings
from .tasks import send_emails, payement_completed
from django.views.decorators.csrf import csrf_exempt
import stripe


from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint # type: ignore
import os
import json

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html', {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response


def order_create(request):
    cart = Cart(request) 
    success = False
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order          = order,
                    product        = item['variation'],
                    original_price = item['original_price'],
                    sale_price     = item['final_price'],  # <-- This is now coupon-aware
                    quantity       = item['quantity'],
                ) 
            success = True 
            cart.clear() 

            send_emails.delay(order.id, form.cleaned_data['email']) #task celery
            #return redirect('orders:pay_order', order_id=order.id)
            # 🔁 Redirect to Stripe checkout
            #return redirect('orders:create_stripe_session', order_id=order.order_id)
            return redirect('orders:order_payment', order_id=order.order_id)

        return render(request, 'orders/created.html', {'order':order, 'success':success})
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/created.html', {'form':form, 'cart':cart})
    

# payment page view (GET)
def order_payment(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'orders/payment.html', {'order': order})

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_session(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    cart = Cart(request)

    coupon_id = str(cart.coupon.id) if cart.coupon else ""

    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.product.name,
                },
                'unit_amount': int(item.sale_price * 100),
            },
            'quantity': item.quantity,
        })

    try:
        session = stripe.checkout.Session.create(
            payment_method_types = ["card"],
            customer_email       = request.user.email if request.user.is_authenticated else order.email,
            line_items=line_items,
            mode="payment",
            success_url = f"http://localhost:8000/fr/orders/payment_success?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.order_id}",
            cancel_url  = "http://localhost:8000/fr/orders/payment_failed",
            metadata={
                'order_id': order.order_id,
                'coupon_id': coupon_id,
            },
        )
        return JsonResponse({"checkout_url":session.url})
    
    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)

def payment_success(request):
    session_id  = request.GET.get("session_id")
    order_id = request.GET.get("order_id")

    if not session_id or not order_id:
        return JsonResponse({'error':'invalid session'}, status=400)

    try:
        session  = stripe.checkout.Session.retrieve(session_id)
        order = get_object_or_404(Order, order_id=order_id)

        customer_email = session.customer_email or session.customer_details.get("email", "")
        customer_name  = session.customer_details.name

        if session.payment_status == "paid":
            order = get_object_or_404(Order, order_id=order_id)
            payement_completed.delay(order.id)

            if 'coupon_id' in request.session:
                del request.session['coupon_id']
                request.session.modified = True

            return render(request, 'orders/payment_success.html', {'order':order})
        
        
        return JsonResponse({"error":"Payment not completed"}, status=400)
    
    except stripe.error.StripeError as e:
        return JsonResponse({"error":str(e)}, status=400)


def payment_failed(request):
    error_message = request.GET.get("error", "Your payment could not be processed. Please try again")
    return render(request, "orders/payment_failed.html", {'error_message':error_message})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_KEY

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session['metadata']['order_id']
        order = Order.objects.get(order_id=order_id)
        order.paid = True
        order.save()

        for item in order.items.select_related('product'):
            variation = item.product
            if variation.quantity >= item.quantity:
                variation.quantity -= item.quantity
                variation.save()
        

        coupon_id = session.get("metadata", {}).get("coupon_id")  

        if coupon_id:
            coupon = Coupon.objects.get(id=coupon_id)
            coupon.used = True
            coupon.save()

    return JsonResponse({"status": "success"}, status=200)


@login_required
def orders_history(request):
    orders = Order.objects.filter(email= request.user.email)
    return render(request, 'orders/orders_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})











