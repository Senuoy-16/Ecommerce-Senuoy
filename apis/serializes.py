from rest_framework import serializers
from store.models import Variation, Product, Category, Color
from accounts.models import Account


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['name', 'slug', 'image', 'created']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ['name', 'slug', 'description', 'category', 'created_at', 'updated']
        depth = 1

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Variation
        fields = ['product', 'color', 'original_price', 'sale_price', 'status', 'quantity', 'sku', 'barcode']
        depth = 1


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Color
        fields = ['name', 'slug', 'code']



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model        = Account
        fields       = ['first_name', 'last_name', 'email', 'username', 'country', 'password']
        extra_kwargs = {'password': {'write_only':True}}
    
    def create(self, validated_data):
        user = Account.objects.create_user(
            first_name = validated_data['first_name'],
            last_name  = validated_data['last_name'],
            username   = validated_data['username'],
            email      = validated_data['email'],
            country    = validated_data['country'],
            password   = validated_data['password']
        )
        return user
    
    