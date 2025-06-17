from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import re
from django.core.cache import cache

# --- Category ---
class Category(models.Model):
    name    = models.CharField(max_length=250)
    slug    = models.SlugField(unique=True)
    image   = models.ImageField(upload_to='categories/images')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


HEX_COLOR_RE = re.compile(r'^#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$')
# --- Color ---
class Color(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    code = models.CharField(max_length=9, help_text="Hex code like #FF0000")

    def clean(self):
        if not HEX_COLOR_RE.match(self.code):
            raise ValidationError({'code': 'Invalid hex color code format.'})

    def save(self, *args, **kwargs):
        self.full_clean() 
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


# --- Product ---
class Product(models.Model):
    name        = models.CharField(max_length=250)
    slug        = models.SlugField(unique=True)
    description = models.TextField(max_length=1500)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes  = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]


# --- Variation ---
class Variation(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'AV', 'Available'
        DRAFT     = 'DF', 'Draft'

    product              = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    color                = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='variations')
    original_price       = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price           = models.DecimalField(max_digits=8, decimal_places=2)
    status               = models.CharField(max_length=2, choices=Status.choices, default=Status.AVAILABLE)
    quantity             = models.PositiveIntegerField(default=0)
    sku                  = models.CharField(max_length=100, unique=True)
    barcode              = models.CharField(max_length=100, blank=True, null=True)

    def clean(self):
        if self.sale_price > self.original_price:
            raise ValidationError('Sale price cannot exceed original price.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        cache.delete(f'product_{self.id}')

    def __str__(self):
        return f"{self.product.name} - {self.color.name}"


# --- Image ---
class Image(models.Model):
    alt   = models.CharField(max_length=30, blank=True, null=True)
    image = models.ImageField(upload_to='products/images')

    def __str__(self):
        return str(self.image)


# --- VariationImage ---
class VariationImage(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name='variation_images')
    image     = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='image_variations')

    def __str__(self):
        return f"{self.variation} - Image {self.image.id}"



# --- Feature ---
class Feature(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='features')
    name        = models.CharField(max_length=100)
    unit        = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.unit})" if self.unit else self.name


# --- ProductFeatureValue ---
class ProductFeatureValue(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feature_values')
    feature     = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='product_values')    
    data_value  = models.CharField(max_length=255)

    class Meta:
        unique_together = ('product', 'feature')
    
    def __str__(self):
        return f"{self.product.name} - {self.feature.name}"
    