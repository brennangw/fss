

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^addtrader/',views.addtrader, name='addtrader'),
    url(r'^addtrade/',views.addtrade, name='addtrade'),
    url(r'^aggregate/',views.aggregate, name='aggregate'),
]
