# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hw2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_code', models.CharField(max_length=11)),
                ('month', models.CharField(max_length=11)),
                ('year', models.IntegerField()),
                ('price', models.FloatField()),
            ],
            options={
                'db_table': 'market_price',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrderBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_code', models.CharField(max_length=11)),
                ('month', models.CharField(max_length=11)),
                ('year', models.IntegerField()),
                ('buy_or_sell', models.IntegerField()),
                ('lots', models.IntegerField()),
                ('price', models.FloatField()),
                ('trader_id', models.IntegerField()),
                ('trade_id', models.IntegerField()),
            ],
            options={
                'db_table': 'order_book',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filled_id', models.IntegerField(null=True, blank=True)),
                ('filled_time', models.DateTimeField(null=True, blank=True)),
                ('lots', models.IntegerField(null=True, blank=True)),
                ('filled_price', models.FloatField(null=True, blank=True)),
            ],
            options={
                'db_table': 'portfolio',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('product_code', models.CharField(max_length=11)),
                ('month_code', models.CharField(max_length=11)),
                ('year', models.IntegerField()),
                ('lots', models.IntegerField()),
                ('buy_or_sell', models.IntegerField()),
                ('order_type', models.CharField(max_length=11)),
                ('price', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
            options={
                'db_table': 'trade',
                'managed': False,
            },
        ),
    ]
