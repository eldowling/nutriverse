# Generated by Django 3.0.7 on 2020-08-10 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20200810_0558'),
        ('checkout', '0003_auto_20200809_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlineitem',
            name='product_subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product_Subscription'),
        ),
    ]
