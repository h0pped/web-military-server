# Generated by Django 4.0.3 on 2022-04-26 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_item_avg_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=150)),
                ('country', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=200)),
                ('zipCode', models.CharField(max_length=10)),
                ('shipment_method', models.CharField(max_length=50)),
                ('order_status', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Order_Item',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('price', models.FloatField(default=0)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopapp.item')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopapp.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='shopapp.Order_Item', to='shopapp.item'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopapp.user'),
        ),
    ]
