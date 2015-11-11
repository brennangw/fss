

from django.conf.urls import patterns, include, url
from . import views
from django.contrib import admin

urlpatterns = [
	
    url(r'^$',views.index, name='index'),
    url(r'^addtrader/',views.addtrader, name='addtrader'),
    url(r'^addtrade/',views.addtrade, name='addtrade'),
    url(r'^aggregate/',views.aggregate, name='aggregate'),
    url(r'^history/',views.history, name='history'),
    url(r'^portfolio/',views.portfolio, name='portfolio'),
    url(r'^pnl/',views.pnl, name='pnl'),
    url(r'^fill/',views.fill, name='fill'),
    url(r'^ack/',views.fill, name='ack'),
]