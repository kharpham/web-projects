# Generated by Django 4.2.4 on 2023-08-28 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='image',
            field=models.ImageField(blank=True, default='no_image.jpg', upload_to='Image'),
        ),
    ]