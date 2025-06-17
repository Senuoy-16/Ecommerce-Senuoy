from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order 
from .models import LoyaltyPoint
from accounts.models import Account

@receiver(post_save, sender=Order)
def add_loyalty_points(sender, instance, created, **kwargs):
    if instance.paid and not instance.points_added:
        try:
            user = Account.objects.get(email=instance.email)
        except Account.DoesNotExist: 
            raise ValueError(f"Utilisateur avec l'email {instance.email} n'existe pas.")

        points_to_add = int(instance.get_total_cost())

        loyalty, created = LoyaltyPoint.objects.get_or_create(user=user)

        loyalty.add_points(points_to_add)
        instance.points_added = True
        instance.save(update_fields=['points_added'])
