# Generated by Django 3.2.15 on 2025-04-09 13:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0062_alter_order_registered_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderelement',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='orderelement',
            name='quantity',
            field=models.IntegerField(db_index=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='количество'),
        ),
    ]
