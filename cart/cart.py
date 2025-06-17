from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from store.models import Variation
from coupons.models import Coupon


class Cart:
    def __init__(self, request):
        """Initialize the cart with session data."""
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})
        self.session[settings.CART_SESSION_ID] = self.cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, variation, quantity=1, override_quantity=False):
        """Add or update an item in the cart."""
        variation_id = str(variation.id)
        current_quantity = self.cart.get(variation_id, {}).get('quantity', 0)
        new_quantity = quantity if override_quantity else current_quantity + quantity

        if new_quantity > variation.quantity:
            raise ValueError(f"Only {variation.quantity} items in stock.")

        self.cart[variation_id] = {
            'quantity': new_quantity,
            'original_price': str(variation.original_price),
            'sale_price': str(variation.sale_price),
        }
        self.save()

    def remove(self, variation_id):
        """Remove an item from the cart."""
        variation_id = str(variation_id)
        if variation_id in self.cart:
            del self.cart[variation_id]
            self.save()

    def save(self):
        """Mark the session as modified to save changes."""
        self.session.modified = True

    def __iter__(self):
        """Iterate through cart items and attach product info."""
        variation_ids = self.cart.keys()
        variations = Variation.objects.filter(id__in=variation_ids).select_related('product', 'color')

        for variation in variations:
            stored_item = self.cart[str(variation.id)]
            item = stored_item.copy()  # Don't mutate self.cart
            quantity = item['quantity']
            sale_price = Decimal(item['sale_price'])

            item['variation'] = variation
            item['total_original_price'] = Decimal(item['original_price']) * quantity
            item['total_sale_price'] = sale_price * quantity

            if self.coupon:
                discount_rate = Decimal(self.coupon.discount) / Decimal(100)
                discounted_price = sale_price * (1 - discount_rate)
                item['final_price'] = discounted_price.quantize(Decimal('0.01'))
            else:
                item['final_price'] = sale_price

            item['final_price_quantity'] = item['final_price'] * quantity
            yield item


    def __len__(self):
        """Total quantity of items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get(self, variation_id):
        """Get a specific cart item by variation ID."""
        return self.cart.get(str(variation_id))

    def get_total_quantity(self):
        """Get total number of products."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_original_price(self):
        """Get total original (non-discounted) price."""
        return sum(Decimal(item['original_price']) * item['quantity'] for item in self.cart.values())

    def get_total_discounted_price(self):
        """Get total discounted price (before coupon)."""
        return sum(Decimal(item['sale_price']) * item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        """Get valid coupon if exists."""
        if self.coupon_id:
            try:
                coupon = Coupon.objects.get(id=self.coupon_id)
                if coupon.used:
                    self.session.pop('coupon_id', None)
                    self.save()
                    return None
                return coupon
            except Coupon.DoesNotExist:
                self.session.pop('coupon_id', None)
                self.save()
        return None

    def get_discount(self):
        """Get the coupon discount amount."""
        if self.coupon and self.coupon.discount is not None:
            discount_rate = Decimal(self.coupon.discount) / Decimal(100)
            return (discount_rate * self.get_total_discounted_price()).quantize(Decimal('0.01'))
        return Decimal('0.00')

    def get_total_price_after_coupons(self):
        """Get the total price after applying coupon discount."""
        total = self.get_total_discounted_price() - self.get_discount()
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def get_variation_ids(self):
        """Get a list of variation IDs in the cart."""
        return list(self.cart.keys())

    def clear(self):
        """Empty the cart."""
        self.session[settings.CART_SESSION_ID] = {}
        self.save()
