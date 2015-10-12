from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Clients, Trades
import csv
from django.db import connection


# Create your views here.

def index(request):
    return render(request, 'hw1/index.html')

def newTradePage(request):
    return render(request, 'hw1/newTrade.html')

def newTraderPage(request):
    return render(request, 'hw1/newTrader.html')

def aggregatePage(request):
    return render(request, 'hw1/aggregate.html')

def historyPage(request):
	return rener(request, 'hw1/history.html')

def addtrader(request):
    first=request.POST['firstname']
    last=request.POST['lastname']
    comp=request.POST['company']

    new = Clients(first_name = first, last_name= last, company = comp)
    new.save()

    return render(request, 'hw1/index.html')

def addtrade(request):

    time=request.POST['time']
    product=request.POST['product']
    month=request.POST['month']
    year=request.POST['year']
    lots=request.POST['lots']
    price=request.POST['price']
    sign=request.POST['sign']
    trader= Clients.objects.get(id=request.POST['trader'])

    new = Trades(time = time, product_code = product, month_code = month, year = year, lots = lots, price = price, buy_or_sell = sign, trader = trader)
    new.save()

    return render(request, 'hw1/index.html')

def aggregate(request):

    traderid=request.POST['traderid']
    cursor=connection.cursor()
    if (traderid == ""):
        cursor.execute("select CONCAT(product_code, month_code, year),sum(lots*buy_or_sell) from trades group by product_code, month_code, year")
    else:
        cursor.execute("select CONCAT(product_code, month_code, year),sum(lots*buy_or_sell) from trades where trader=%s group by product_code, month_code, year",[traderid])

    aggregate_position = cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aggregate.csv"'
    writer = csv.writer(response)
    for i in range(len(aggregate_position)):
        writer.writerow(aggregate_position[i])
    return response

def history(request):
	traderid=request.POST['traderid']
	cursor=connection.cursor()
	if (traderid == ""):
		cursor.execute("select * from trades group by product_code, month_code, year")
	else: 
		cursor.execute("select * from trades where trader= %s group by product_code, month_code, year",[traderid])
	aggregate_position = cursor.fetchall()
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachement; filename="aggregate.csv"'
	writer = csv.writer(response)
	for i in range(len(aggregate_position)):
		writer.writerow(aggregate_position[i]);
	return response


