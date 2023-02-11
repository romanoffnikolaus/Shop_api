from .models import Product, Category
from review.models import Rating, Comment
from rest_framework import serializers
from review.serializers import RatinfSerializer, CommentSerializer
from django.db.models import Avg


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Стоимость товара не можеть быть отрицательной. Что там с деньгами?')
        return price

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = (i['body'] for i in CommentSerializer(Comment.objects.filter(product=instance.pk), many=True).data)
        representation['ratings'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        representation['likes'] = instance.likes.count()
        return representation


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
