# Generated by Django 4.2.7 on 2023-11-12 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
