from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account
from django.core.mail import send_mail
from django.conf import settings
from loyalty.models import LoyaltyPoint

@receiver(post_save, sender=Account)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        #to create a loyaltypoint and starting by zero point
        loyalty, created = LoyaltyPoint.objects.get_or_create(user=instance)
        loyalty.add_points(0)

        subject = 'Welcome to Senuoy E-commerce Website'
        message = f'Hi {instance.username}, \n thank you for creating an account with us'
        from_email = settings.DEFAULT_FROM_EMAIL
        user_email = [instance.email]

        send_mail(subject, message, from_email, user_email)