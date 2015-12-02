

from django.conf.urls import patterns, include, url
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^addSwap/',views.addSwap, name='addSwap'),
    url(r'^EOD/',views.EODProcess, name='EOD'),
]
