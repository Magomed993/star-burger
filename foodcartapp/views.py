import json
from logging import exception

from phonenumber_field.phonenumber import PhoneNumber
from django.http import JsonResponse
from django.template.defaultfilters import first, lower
from django.templatetags.static import static
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.serializers import ModelSerializer, ListField


from .models import Product
from .models import Order
from .models import OrderElement


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    products_serializer = serializer.validated_data['products']
    for item in products_serializer:
        product = Product.objects.filter(name=item.get('product')).first()
        item.update({
            'id': product.id,
            'name': product.name,
            'category': {
                'id':product.category.id,
                'name': product.category.name
            },
            'image': product.image.url,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description
        })
    for item in products_serializer:
        product = Product.objects.filter(name=item.get('product')).first()
        order, created = Order.objects.get_or_create(
            address=serializer.validated_data['address'],
            firstname=serializer.validated_data['firstname'],
            lastname=serializer.validated_data['lastname'],
            phonenumber=serializer.validated_data['phonenumber']
        )
        order_element, el_created = OrderElement.objects.get_or_create(
            order=order,
            product=product,
            defaults={
                'quantity': item['quantity']
            }
        )
    return Response({'good': 'status good - 200'}, status=status.HTTP_200_OK)


class OrderElementSerializer(ModelSerializer):
    class Meta:
        model = OrderElement
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = ListField(child=OrderElementSerializer(), allow_empty=False)
    class Meta:
        model = Order
        fields = ['address', 'firstname', 'lastname', 'phonenumber', 'products']
