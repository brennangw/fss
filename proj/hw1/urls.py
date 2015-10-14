

from django.conf.urls import patterns, include, url
from . import views
from django.contrib import admin

urlpatterns = [
	
    url(r'^$',views.index, name='index'),
    url(r'^newTrader/', views.newTraderPage, name='newTraderPage'),
    url(r'^newTrade/', views.newTradePage, name='newTradePage'),
    url(r'^requestAggregate/', views.aggregatePage, name='aggregatePage'),
    url(r'^addtrader/',views.addtrader, name='addtrader'),
    url(r'^addtrade/',views.addtrade, name='addtrade'),
    url(r'^aggregate/',views.aggregate, name='aggregate'),
    url(r'^history/',views.history, name='history'),
]
