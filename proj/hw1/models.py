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
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    company = models.TextField(db_column='Company', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'clients'

class Trades(models.Model):
    time = models.DateTimeField(blank=True, null=True)
    symbol = models.TextField(blank=True, null=True)
    product_code = models.IntegerField(blank=True, null=True)
    month_code = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    lots = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    buy_or_sell = models.IntegerField(blank=True, null=True)
    trader = models.ForeignKey(Clients, db_column='trader')

    class Meta:
        managed = False
        db_table = 'trades'
