# Generated by Django 4.2.4 on 2023-08-31 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_alter_auctionlisting_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
