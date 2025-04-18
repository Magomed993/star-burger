import requests

from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.conf import settings

from environs import Env
from geopy import distance

from foodcartapp.models import Product, Restaurant, Order
from places.models import Place


env = Env()
env.read_env()


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = Order.objects.total_price()
    restaurants = Restaurant.objects.all()

    for order in orders:
        for item in order.order_elements.select_related('product'):
            accept_restaurants = item.product.menu_items \
                .prefetch_related('restaurant', 'product')\
                .values_list('restaurant__name', flat=True)
        order.restaurants = accept_restaurants
        order_place, created = Place.objects.get_or_create(
            address=order.address,
        )
        order_coordinates = fetch_coordinates(settings.API_KEY, order.address)
        order_place.lat, order_place.lng = order_coordinates
        order_place.save()

        try:
            restaurants_distances = []
            for order_restaurant in order.restaurants:
                restaurant = restaurants.get(name=order_restaurant)
                restaurant_place, created_ = Place.objects.get_or_create(
                    address=restaurant.address,
                )
                if created_:
                    coordinates_restaurant = fetch_coordinates(settings.API_KEY, order_restaurant)
                    restaurant_place.lat, restaurant_place.lng = coordinates_restaurant
                    restaurant_place.save()
                restaurant_distance = round(
                    distance.distance(
                        (
                            order_place.lat,
                            order_place.lng
                        ),
                        (
                            restaurant_place.lat,
                            restaurant_place.lng
                        )
                    ).km, 2
                )
                restaurants_distances.append((order_restaurant, restaurant_distance))
            restaurants_distances = sorted(restaurants_distances, key=lambda dist: dist[1])
            order.restaurant_distances = restaurants_distances
        except requests.exceptions.RequestException as err:
            print(err)


    return render(request, template_name='order_items.html', context={
        'order_items': orders,
    })
