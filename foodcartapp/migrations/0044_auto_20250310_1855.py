# Generated by Django 3.2.15 on 2025-03-10 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_auto_20250305_2007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='last_name',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='mobile_number',
            new_name='phonenumber',
        ),
    ]
