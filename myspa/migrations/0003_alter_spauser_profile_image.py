# Generated by Django 5.0.6 on 2024-05-31 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myspa', '0002_remove_spauser_wallet_spauser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spauser',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_image/'),
        ),
    ]
