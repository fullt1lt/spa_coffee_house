# Generated by Django 5.0.6 on 2024-06-18 15:27

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myspa', '0015_alter_typecategories_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='typecategories',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='typecategories',
            name='price',
        ),
        migrations.CreateModel(
            name='MassageSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DurationField(choices=[(datetime.timedelta(seconds=3600), 'Regular'), (datetime.timedelta(seconds=5400), 'Long')])),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('type_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='myspa.typecategories')),
            ],
        ),
    ]
