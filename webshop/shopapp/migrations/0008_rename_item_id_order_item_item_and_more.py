# Generated by Django 4.0.3 on 2022-04-26 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_order_order_item_order_items_order_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_item',
            old_name='item_id',
            new_name='item',
        ),
        migrations.RenameField(
            model_name='order_item',
            old_name='order_id',
            new_name='order',
        ),
    ]
