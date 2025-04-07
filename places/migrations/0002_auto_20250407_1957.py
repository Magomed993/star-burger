# Generated by Django 3.2.15 on 2025-04-07 19:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.CharField(max_length=100, unique=True, verbose_name='адрес места'),
        ),
        migrations.AlterField(
            model_name='place',
            name='date',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='дата'),
        ),
        migrations.AlterField(
            model_name='place',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='широта'),
        ),
        migrations.AlterField(
            model_name='place',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='долгота'),
        ),
    ]
