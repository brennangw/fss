from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Clients, Trade, Portfolio, Swaps, PythonServers
import csv
from django.db import connection
import time
import requests
# Create your views here.

thisServerUrl = "http://localhost:8000"

def getUpServer(urlSnippet):
    for server in PythonServers.objects.all():
        if server.status == 1:
            return HttpResponseRedirect(server.address + '/' + urlSnippet)
    return HttpResponseRedirect(thisServerUrl)

def index(request):
    return render(request, 'lb/index.html')

def addSwap(request):
    return getUpServer('hw4/addSwap')
 
def EODProcess(request):
    return getUpServer('hw4/EOD')

def addtrader(request):
    return getUpServer('hw4/addtrader')

def addtrade(request):
    return getUpServer('hw4/addtrade')

def aggregate(request):
    return getUpServer('hw4/aggregate')

def history(request):
    return getUpServer('hw4/history')

def pnl(request):
    return getUpServer('hw4/pnl')

def portfolio(request):
    return getUpServer('hw4/portfolio')

def pnlbytrade(request):
    return getUpServer('hw4/pnlbytrade')

def pnlbytrader(request):
    return getUpServer('hw4/pnlbytrader')

def pnlbyproduct(request):
    return getUpServer('hw4/pnlbyproduct')
