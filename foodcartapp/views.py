import json

from django.http import JsonResponse
from django.template.defaultfilters import first
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
    # TODO это лишь заглушка
    # orders = json.loads(request.body.decode())
    orders = request.data
    for item in orders['products']:
        product = Product.objects.filter(id=item.get('product')).first()
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
    for item in orders['products']:
        product = Product.objects.filter(id=item.get('product')).first()
        order, created = Order.objects.get_or_create(
            address=orders['address'],
            name=orders['firstname'],
            last_name=orders['lastname'],
            mobile_number=orders['phonenumber']
        )
        order_element, el_created = OrderElement.objects.get_or_create(
            order=order,
            product=product,
            defaults={
                'quantity': item['quantity']
            }
        )
    return Response({})
