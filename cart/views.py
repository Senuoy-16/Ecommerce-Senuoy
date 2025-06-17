from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Variation
from django.views.decorators.http import require_POST
from cart.forms import CartAddProductForm
from coupons.forms import CouponApplyForm



#i dont want to redirect to any page just add the variation to my cart
def add_to_cart(request, variation_id):
    cart = Cart(request)
    variation = get_object_or_404(Variation, id=variation_id)
    cart.add(variation, quantity=1)
    return redirect('cart:cart_detail')

def add_from_form(request, variation_id):
    cart = Cart(request)
    variation = get_object_or_404(Variation, id=variation_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(variation, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')

def remove_from_cart(request, variation_id):
    cart = Cart(request)
    cart.remove(variation_id)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    cart_product_form = CartAddProductForm()
    context = {
        'cart':cart,
        'cart_product_form':cart_product_form,
        'coupon_apply_form':CouponApplyForm,

    }
    return render(request, 'cart/cart_details.html', context)