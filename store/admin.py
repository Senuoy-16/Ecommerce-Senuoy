from django.contrib import admin
from .models import (
    Category, Color, Product, Variation, Image,
    VariationImage, Feature, ProductFeatureValue
)


# Inline for uploading images directly within Variation admin
class VariationImageInline(admin.TabularInline):  
    model = VariationImage
    extra = 1 
    autocomplete_fields = ['image'] 


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created')
    search_fields = ('name',)
    readonly_fields = ['slug']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'code')
    search_fields = ('name',)
    readonly_fields = ['slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'created_at', 'updated')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ['slug']


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'original_price', 'sale_price', 'quantity', 'status', 'sku')
    list_filter = ('status', 'color')
    search_fields = ('product__name', 'sku')
    inlines = [VariationImageInline]  


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    search_fields = ('image',)


@admin.register(VariationImage)
class VariationImageAdmin(admin.ModelAdmin):
    list_display = ('variation', 'image')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit')
    search_fields = ('name',)





@admin.register(ProductFeatureValue)
class ProductFeatureValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'feature', 'data_value')
    search_fields = ('product__name', 'feature__name', 'data_value')
