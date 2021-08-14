# Generated by Django 3.1.8 on 2021-08-14 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210812_2022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='watchlist',
        ),
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='auction_listing', to='auctions.auctionlisting'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bid',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auctions', models.ManyToManyField(blank=True, related_name='auctions_in_the_watchlist', to='auctions.AuctionListing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
