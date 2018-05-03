from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
	lookup_field = 'slug'
	
	class Meta:
		model = Product
		fields = ('id',
			'name',
				'slug',
				'description',
				'active',
				'price',
				'stock',
				'barcode',
				'brand',)
				