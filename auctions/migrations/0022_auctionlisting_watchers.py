# Generated by Django 4.2.4 on 2023-08-30 02:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_alter_auctionlisting_current_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='watchers',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]