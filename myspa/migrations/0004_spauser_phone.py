# Generated by Django 5.0.6 on 2024-06-03 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myspa', '0003_alter_spauser_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='spauser',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
