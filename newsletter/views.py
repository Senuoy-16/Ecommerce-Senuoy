from django.shortcuts import render, redirect
from .forms import SubscriberForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            context = { 'email':subscriber.email}
            email_content = render_to_string('newsletter/subscription_thank_you.html', context)

            email_subject  = 'Thank you for subscription'
            recipient_list = [subscriber.email]
            from_email     = settings.DEFAULT_FROM_EMAIL
            send_mail(
                email_subject,
                '',
                from_email,
                recipient_list,
                html_message=email_content,
                fail_silently=False,
            )

            
            # Show a success message if you want
        return redirect(request.META.get('HTTP_REFERER', '/'))















