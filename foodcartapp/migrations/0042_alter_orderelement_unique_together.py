# Generated by Django 3.2.15 on 2025-02-16 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_rename_orderelements_orderelement'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderelement',
            unique_together={('order', 'product')},
        ),
    ]
