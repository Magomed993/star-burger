# Generated by Django 3.2.15 on 2025-02-14 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_order_orderelements'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderelements',
            name='order',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='order_elements', to='foodcartapp.order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderelements',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_elements', to='foodcartapp.product', verbose_name='товар'),
        ),
    ]
