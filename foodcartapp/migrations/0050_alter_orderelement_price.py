# Generated by Django 3.2.15 on 2025-03-18 16:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0049_orderelement_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderelement',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена'),
        ),
    ]
