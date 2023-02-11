from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Order, OrderItem
from product.models import Product
from .models import Favorite


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True) #для того, чтоб из атемов заказа закидыывать товары 
    class Meta:
        model = Order
        fields = ['id', 'created_at', 'total_sum', 'items']

    def create(self,validated_data):
        items = validated_data.pop('items')
        validated_data['author'] = self.context.get('request').user
        # print(self.context.get('request'))
        order = super().create(validated_data)
        total_sum = 0
        order_items = []
        for i in items:
            order_items.append(OrderItem(order=order, product=i['product'], quantity=i['quantity']))
            total_sum+=i['product'].price * i['quantity']
        OrderItem.objects.bulk_create(order_items)
        order.total_sum = total_sum
        order.save()
        return order

class FavoriteSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    product = ReadOnlyField()

    class Meta:
        model = Favorite
        fields = '__all__'

    