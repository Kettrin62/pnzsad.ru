# Generated by Django 3.2 on 2022-03-01 19:04

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20220227_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phoneNumber',
            field=phonenumber_field.modelfields.PhoneNumberField(default='4.2.3.8.9.9.9.0.9.2.9.9.e164.arpa', max_length=128, region=None, verbose_name='Телефон'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
