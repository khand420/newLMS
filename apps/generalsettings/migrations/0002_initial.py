# Generated by Django 5.0 on 2024-01-25 09:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('generalsettings', '0001_initial'),
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tellycommsettings',
            name='source_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.sources'),
        ),
    ]
