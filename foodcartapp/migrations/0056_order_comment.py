# Generated by Django 3.2.15 on 2025-03-20 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0055_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='комментарий'),
        ),
    ]
