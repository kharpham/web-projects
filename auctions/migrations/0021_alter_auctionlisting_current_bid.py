# Generated by Django 4.2.4 on 2023-08-29 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_alter_auctionlisting_current_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='current_bid',
            field=models.FloatField(blank=True, verbose_name='Current bid($)'),
        ),
    ]
