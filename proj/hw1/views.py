from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Clients, Trades
import csv
from django.db import connection
import time
import requests


# Create your views here.

def index(request):
    """
    Main page of the application, and has all of the forms required to 

    1. Create entries to :model:`hw1.Clients` and :model:`hw1.Trades`.
    2. Get verious aggregates and histories from these 2 models.

    """
    return render(request, 'hw1/index.html')

def newTradePage(request):
    """
    Page specific to adding a new trade to :model:`hw1.Trades`.

    """
    return render(request, 'hw1/newTrade.html')

def newTraderPage(request):
    """
    Page specific to adding a new trader to :model:`hw1.Clients`.

    """
    return render(request, 'hw1/newTrader.html')

def aggregatePage(request):
    """
    Page specific to requesting the aggregate position of a single trader, or the overall aggregate from :model:`hw1.Trades`.

    """
    return render(request, 'hw1/aggregate.html')

def historyPage(request):
    """
    Page specific to requesting the trade history of a single trader, or the overall trade history from :model:`hw1.Trades`.

    """
    return render(request, 'hw1/history.html')

def addtrader(request):
    """
    API interface: Request handler for adding a new trader to :model:`hw1.Clients`.

    Required parameters:

        1. Product code
        2. Month of contract expiry
        3. Year of contract expiry
        4. Number of lots
        5. Price per lot
        6. Buy/Sell (one of these as text)
        7. Assigned trader_ID of the trader

    """
    first=request.POST['firstname']
    last=request.POST['lastname']
    comp=request.POST['company']

    new = Clients(first_name = first, last_name= last, company = comp)
    new.save()

    return HttpResponseRedirect('/hw1/?success=true')

def addtrade(request):
    """
    API interface: Request handler for adding a new trade to :model:`hw1.Trades`.

    Required parameters:

        1. First name of the trader
        2. Last name of the trader
        3. Company the trader belongs to

    """
    date_time=time.strftime('%Y-%m-%d %H:%M:%S')
    product=request.POST.get('product', False)
    month=request.POST.get('month', False)
    year=request.POST.get('year', False)
    lots=request.POST.get('lots', False)
    price=request.POST.get('price', False)
    sign=''
    if request.POST.get('sign', False) == 'Buy':
        sign=1
    else:
        sign=-1
    trader= Clients.objects.get(id=request.POST.get('trader', False))
    side = request.POST.get('sign', False).lower();
    type = request.POST.get('type', False)
    post_data = {'type': type, 'side': side, 'symbol': product, 'price': price, 'lots' : lots}
    new = Trades(status = 0; time = date_time, product_code = product, month_code = month, year = year, lots = lots, price = price, buy_or_sell = sign, trader = trader)
	id = Trades.objects.latest('id');
    post_data = {'id': id, 'type': type, 'side': side, 'symbol': product, 'price': price, 'lots' : lots}
    requests.post('localhost:8080/fix/process-order', data=post_data)
    new.save()
	return HttpResponseRedirect('/hw1/?success=true')

def fixAck(request):
    tradeid = request.POST.get('id', False)
    trade = Trades.objects.get(id=tradeid)
    trade.status = 2;
    trade.save();

def fill(request):
    tradeid = request.POST.get('id', False)
	trade = Trades.objects.get(id=tradeid)
	trade.status = 4;
	trade.save();
	

def exchangeAck(request):
    tradeid = request.POST.get('id', False)
	trade = Trades.objects.get(id=tradeid)
	trade.status = 3;
	trade.save();

def aggregate(request):
    """
    API interface: Request handler for getting the aggregate position of a single trader, or the overall aggregate position from :model:`hw1.Trades`.

        Required parameters: Trader_ID (unique ID or a blank field)

    """
    traderid=request.POST['traderid']
    cursor=connection.cursor()
    if (traderid == ""):
        cursor.execute("select product_code, month_code, year,sum(lots*buy_or_sell) from trades group by product_code, month_code, year")
        header=['Product','Month','Year','Aggregate']
    else:
        cursor.execute("select product_code, month_code, year,sum(lots*buy_or_sell) from trades where trader=%s group by product_code, month_code, year",[traderid])
        header=['Product','Month','Year','Aggregate']

    aggregate_position = cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aggregate.csv"'
    writer = csv.writer(response)
    writer.writerow(header)
    for i in range(len(aggregate_position)):
        writer.writerow(aggregate_position[i])
    
    return response

def history(request):
    """
    API interface: Request handler for getting the trade history of a single trader, or all trade histories from :model:`hw1.Trades`.

        Required parameters: Trader_ID (unique ID or a blank field)

    """
    traderid=request.POST['traderid']
    cursor=connection.cursor()
    if (traderid == ""):
        cursor.execute("select * from trades")
        header=['Trade_ID','Time','Product','Month','Year','Lots','Price (in cents)','Buy(+1)/Sell(-1)','Trader_ID']
    else: 
        cursor.execute("select * from trades where trader= %s",[traderid])
        header=['Trade_ID','Time','Product','Month','Year','Lots','Price (in cents)','Buy(+1)/Sell(-1)','Trader_ID']
    aggregate_position = cursor.fetchall()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename="aggregate.csv"'
    writer = csv.writer(response)
    writer.writerow(header)
    for i in range(len(aggregate_position)):
        writer.writerow(aggregate_position[i]);
    return response
