# Generated by Django 5.0.6 on 2024-06-21 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myspa', '0027_alter_spauser_name_alter_spauser_surname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spauser',
            name='name',
        ),
        migrations.RemoveField(
            model_name='spauser',
            name='surname',
        ),
    ]
