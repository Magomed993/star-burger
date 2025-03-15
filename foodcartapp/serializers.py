from rest_framework.serializers import ModelSerializer, ListField
from foodcartapp.models import Order, OrderElement


class OrderElementSerializer(ModelSerializer):
    class Meta:
        model = OrderElement
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = ListField(child=OrderElementSerializer(), allow_empty=True, write_only=True)
    class Meta:
        model = Order
        fields = ['id', 'address', 'firstname', 'lastname', 'phonenumber', 'products']
