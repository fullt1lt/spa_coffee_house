# Generated by Django 5.0.6 on 2024-06-12 21:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myspa', '0010_spaсategories_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='massagetherapist',
            name='average_rating',
            field=models.FloatField(default=5.0),
        ),
        migrations.AddField(
            model_name='massagetherapist',
            name='type_categories',
            field=models.ManyToManyField(related_name='masseurs', to='myspa.typecategories'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='myspa.massagetherapist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
