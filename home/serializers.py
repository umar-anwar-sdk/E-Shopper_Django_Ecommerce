from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Brand, Category, Order, Product

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(source='Category', read_only=True)
    brand = serializers.StringRelatedField(read_only=True)
    vendor = serializers.StringRelatedField(read_only=True)
    vendor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='vendor'),
        source='vendor',
        write_only=True,
        required=False,
        allow_null=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='Category',
        write_only=True,
        required=False,
        allow_null=True
    )
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        source='brand',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'details', 'price', 'Availability', 'Condition',
            'date', 'image', 'Category', 'category', 'category_id',
            'brand', 'brand_id', 'vendor', 'vendor_id'
        ]
        read_only_fields = ['id', 'date', 'category', 'brand', 'vendor']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'user', 'quantity', 'price', 'address', 'phone', 'pincode', 'total', 'image', 'date']
        read_only_fields = ['id', 'user', 'total', 'date']
