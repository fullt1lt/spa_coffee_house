# Generated by Django 5.0.6 on 2024-06-18 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myspa', '0017_rename_massagesession_cateroriessession'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CateroriesSession',
            new_name='CategoriesSession',
        ),
    ]
