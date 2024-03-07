# Generated by Django 5.0 on 2024-01-24 07:38

import apps.product.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default=apps.product.utils.Status['active'], max_length=255)),
                ('name', models.CharField(max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('product_code', models.CharField(max_length=70, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('conversion_days', models.CharField(max_length=255, null=True)),
                ('client', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
