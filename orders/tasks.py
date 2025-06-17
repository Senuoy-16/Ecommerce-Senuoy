# orders/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import weasyprint
from io import BytesIO #to accelerate the process of sending emails by saving pdfs in memory not in hardware 


@shared_task
def send_emails(order_id, email):
    # Import Order here to avoid circular import issues
    from .models import Order  
    
    order = Order.objects.get(id=order_id)
    
    context = {
        'order': order,
    }
    subject = 'Order Confirmation'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    html_message = render_to_string('orders/confirmation_order.html', context)
    text_message = f"Your order ID: {order.order_id} has been created successfully."
    
    email = EmailMultiAlternatives(subject, text_message, email_from, recipient_list)
    email.attach_alternative(html_message, "text/html")
    email.send()



@shared_task
def payement_completed(order_id):
    order=Order.objects.get(id=order_id)

    subject = f"Senuoy - Invoice. {order.order_id}"
    message = f'hello {order.get_full_name()}, \n Please find attached the invoice for your recent purchase'
    from_email = settings.DEFAULT_FROM_EMAIL
    email_user = [order.email]

    html = render_to_string('orders/pdf.html', {'order':order})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out)
 
    email = EmailMessage(
        subject=subject,
        body = message,
        from_email=from_email,
        to=email_user
    )
    email.attach(f'order_{order.order_id}.pdf', out.getvalue(), 'application/pdf')
    email.send()
    return True