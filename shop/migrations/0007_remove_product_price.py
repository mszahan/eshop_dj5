# Generated by Django 5.0.8 on 2024-09-24 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_variation_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
    ]
