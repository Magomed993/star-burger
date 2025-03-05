import json

from django.core.management.base import BaseCommand
from foodcartapp.models import Product, ProductCategory


with open('products.json', 'r') as file:
    data = json.load(file)


class Command(BaseCommand):
    help = 'Скачивание бургеров через файл'

    def handle(self, *args, **options):
        for burger in data:
            obj, created = Product.objects.update_or_create(
                name=burger['title'],
                category=ProductCategory.objects.filter(name__contains=burger['type']).first(),
                price=burger['price'],
                image=burger['img'],
                description=burger['description']
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Добавлен: {obj}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Обновлен: {obj}"))
