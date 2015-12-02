

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
    url(r'^pnlbytrade/',views.pnlbytrade, name='pnlbytrade'),
    url(r'^pnlbytrader/',views.pnlbytrader, name='pnlbytrader'),
    url(r'^pnlbyproduct/',views.pnlbyproduct, name='pnlbyproduct'),
    url(r'^exchange-message/',views.exchange_message, name='message-from-exchange')
]
