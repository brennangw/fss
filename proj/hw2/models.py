# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Clients(models.Model):
    """
    Stores information about all traders in :model:`hw1.Clients`.

    """
    
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    company = models.TextField(db_column='Company', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'clients'

class Trades(models.Model):
    """
    Records each trade entered in :model:`hw1.Trades`.

    Each trade recorded links to a trader in :model:`hw1.Clients`.

    """

    time = models.DateTimeField(blank=True, null=True)
    product_code = models.TextField(blank=True, null=True)
    month_code = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    lots = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    buy_or_sell = models.IntegerField(blank=True, null=True)
    trader = models.ForeignKey(Clients, db_column='trader')

    class Meta:
        managed = False
        db_table = 'trade'


class MarketPrice(models.Model):
    """
    Records each trade entered in :model:`hw2.Trades`.

    Each trade recorded links to a trader in :model:`hw2.Clients`.

    """
    product_code = models.CharField(max_length=11)
    month = models.CharField(max_length=11)
    year = models.IntegerField()
    price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'market_price'


class OrderBook(models.Model):
    """
    Records the trade book in the exchange in :model:`hw2.OrderBook`

    Each row represents an item listed on the exchange.

    """
    product_code = models.CharField(max_length=11)
    month = models.CharField(max_length=11)
    year = models.IntegerField()
    buy_or_sell = models.IntegerField()
    lots = models.IntegerField()
    price = models.FloatField()
    trader_id = models.IntegerField()
    trade_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_book'


class Portfolio(models.Model):
    """
    Records the portfolio the clients has from the filled messages sent from the exhange

    Each row represents a fill message according to a specific trade either partial or final.

    """
    id = models.ForeignKey('Trade', db_column='id', primary_key=True)
    trade_id = models.IntegerField()
    filled_id = models.IntegerField(blank=True, null=True)
    lots = models.IntegerField(blank=True, null=True)
    filled_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'portfolio'


class Trade(models.Model):
    """
    New Trade table for HW2, recording the orders submitted with the order type added in.

    Each row represent a submitted order either active or historically executed.

    """
    time = models.DateTimeField()
    product_code = models.CharField(max_length=11)
    month_code = models.CharField(max_length=11)
    year = models.IntegerField()
    lots = models.IntegerField()
    buy_or_sell = models.IntegerField()
    order_type = models.CharField(max_length=11)
    price = models.IntegerField()
    trader = models.ForeignKey(Clients, db_column='trader')

    class Meta:
        managed = False
        db_table = 'trade'
