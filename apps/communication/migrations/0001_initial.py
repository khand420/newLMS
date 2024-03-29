# Generated by Django 3.2.11 on 2023-07-10 11:31

import communication.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default=communication.utils.Status['active'], max_length=255)),
                ('title', models.CharField(max_length=70, null=True)),
                ('description', models.CharField(max_length=70, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('client_id', models.CharField(max_length=255, null=True)),
                ('type', models.CharField(choices=[('google', 'google'), ('facebook', 'facebook')], max_length=255, null=True)),
            ],
        ),
    ]
