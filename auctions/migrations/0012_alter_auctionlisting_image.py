# Generated by Django 4.2.4 on 2023-08-28 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auctionlisting_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]