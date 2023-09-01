# Generated by Django 4.2.4 on 2023-08-28 02:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_comment_auctionlisting'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='creater',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='starting_bid',
            field=models.IntegerField(verbose_name='Starting bid'),
        ),
    ]