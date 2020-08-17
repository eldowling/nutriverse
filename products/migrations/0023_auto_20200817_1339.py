# Generated by Django 3.0.7 on 2020-08-17 13:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20200816_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(default=datetime.datetime(2020, 8, 17, 13, 39, 13, 635460, tzinfo=utc), max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='product_subscription',
            name='code',
            field=models.CharField(default=datetime.datetime(2020, 8, 17, 13, 39, 13, 636776, tzinfo=utc), max_length=20, unique=True),
        ),
    ]
