from django.shortcuts import render, get_object_or_404
from .models import Product, Variation, Category
from cart.forms import CartAddProductForm
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch

def list_product(request):
    categories = Category.objects.all()

    available_variations = Variation.objects.filter(
        status=Variation.Status.AVAILABLE,
        quantity__gt=0
    ).select_related('color').prefetch_related('variation_images__image')

    products = Product.objects.filter(
        variations__in=available_variations
    ).prefetch_related(
        Prefetch('variations', queryset=available_variations),
    ).distinct()

    paginator   = Paginator(products, 4)  # u can change easily how much product you want to show it in page
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products'  : page_obj,
        'page_obj'  : page_obj,
    }
    return render(request, 'store/list_product.html', context)


def home(request):
    categories = Category.objects.all()

    available_variations = Variation.objects.filter(
        status=Variation.Status.AVAILABLE,
        quantity__gt=0
    ).select_related('color').prefetch_related('variation_images__image')

    products = Product.objects.filter(
        variations__in=available_variations
    ).prefetch_related(
        Prefetch('variations', queryset=available_variations),
    ).distinct()[:4]

    context = {
        'categories':categories,
        'products': products,
    }
    return render(request, 'store/home.html', context)


def product_by_category(request, category_slug):
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            variations__status=Variation.Status.AVAILABLE,
            variations__quantity__gt=0,
            category = category,
        ).prefetch_related(
            'variations__color',
            'variations__variation_images__image'
        ).distinct()
    
    context = {
        'category':category,
        'products':products
    }
    return render(request, 'store/product_by_category.html', context)


def product_detail(request, variation_id):
    cache_key = f'product_{variation_id}' 
    variation = cache.get(cache_key)
    if variation is None:
        variation = get_object_or_404(
            Variation.objects.select_related('product', 'color').prefetch_related('variation_images__image'),
            id=variation_id
        )
        cache.set(cache_key, variation, 60*30)

    product = variation.product  # Get the parent product

    cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'variation': variation,
        'cart_product_form':cart_product_form,
    }
    return render(request, 'store/product_detail.html', context)

