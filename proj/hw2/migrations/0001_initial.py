# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.TextField(null=True, blank=True)),
                ('last_name', models.TextField(null=True, blank=True)),
                ('company', models.TextField(null=True, db_column='Company', blank=True)),
            ],
            options={
                'db_table': 'clients',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(null=True, blank=True)),
                ('symbol', models.TextField(null=True, blank=True)),
                ('product_code', models.IntegerField(null=True, blank=True)),
                ('month_code', models.IntegerField(null=True, blank=True)),
                ('year', models.IntegerField(null=True, blank=True)),
                ('lots', models.IntegerField(null=True, blank=True)),
                ('price', models.IntegerField(null=True, blank=True)),
                ('buy_or_sell', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'trades',
                'managed': False,
            },
        ),
    ]
