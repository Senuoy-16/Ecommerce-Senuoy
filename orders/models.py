from django.db import models
import random
import string
from django.utils import timezone
from store.models import Variation
from accounts.models import Account

def generate_order_id(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

class Order(models.Model):
    order_id     = models.CharField(max_length=8, default=generate_order_id, unique=True)
    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    email        = models.EmailField()
    address      = models.CharField(max_length=200)
    postal_code  = models.PositiveIntegerField()
    city         = models.CharField(max_length=100)
    created_at   = models.DateTimeField(default=timezone.now)
    update_at    = models.DateTimeField(auto_now=True)
    paid         = models.BooleanField(default=False)
    points_added = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at'] 
        indexes  = [
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return f'Order ID: {self.order_id}'

    def get_full_name(self):
        return self.first_name +' '+ self.last_name    
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            unique_id = generate_order_id()
            while Order.objects.filter(order_id=unique_id).exists():
                unique_id = generate_order_id()
            self.order_id = unique_id
        super().save(*args,**kwargs)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_quantity(self):
        return sum(item.quantity for item in self.items.all())
    
class OrderItem(models.Model):
    order          = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product        = models.ForeignKey(Variation, related_name='order_item', on_delete=models.CASCADE)
    original_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price     = models.DecimalField(max_digits=6, decimal_places=2)
    quantity       = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'
    
    def get_cost(self):
        return self.sale_price * self.quantity
