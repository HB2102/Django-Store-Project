# Generated by Django 5.0.2 on 2024-05-02 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_rename_oreder_order_rename_oreritem_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_shippes',
            field=models.BooleanField(default=False),
        ),
    ]
