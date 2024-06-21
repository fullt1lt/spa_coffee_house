# Generated by Django 5.0.6 on 2024-06-20 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myspa', '0020_typeblogandnews_blogandnews'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gallery_image', models.ImageField(blank=True, null=True, upload_to='gallery_image/')),
                ('type_gallery', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='type_gallery', to='myspa.typegallery')),
            ],
        ),
    ]