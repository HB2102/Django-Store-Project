# Generated by Django 5.0.2 on 2024-05-02 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_order_is_shippes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='is_shippes',
            new_name='is_shipped',
        ),
    ]