# Generated by Django 5.0.6 on 2024-06-18 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myspa', '0016_remove_typecategories_duration_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MassageSession',
            new_name='CateroriesSession',
        ),
    ]