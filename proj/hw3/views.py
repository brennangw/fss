from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Clients, Trade, Portfolio, Swaps
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
    return render(request, 'hw3/index.html')

def addSwap(request):
    if request.method == 'POST':
        #TODO: Get the parameters of the swap and enter into the database
        start = request.POST.get('start', False)
        termination = request.POST.get('termination', False)
        fixed = request.POST.get('fixed', False)
        float_idx = request.POST.get('float', False)
        spread = request.POST.get('spread', False)
        notional = request.POST.get('notional', False)
        payer = request.POST.get('payer', False)
        clearing = request.POST.get('clearing', False)
        trader_id = request.POST.get('trader', False)

        trader= Clients.objects.get(id=trader_id)

        new = Swaps(startdate=start, terminationdate=termination, fixedrate=fixed, floatrate=float_idx, floatspread=spread, notional=notional, fixedpayer=payer, clearinghouse=clearing, traderid = trader)
        new.save()

        return HttpResponseRedirect('/hw3/?success=true')

    return render(request, 'hw3/addSwap.html')

def EODProcess(request):
    if request.method == 'POST':
        #TODO: Query database for aggregate, and roll day to the next

        #TODO: Figure out a way to store the calendar, and find the next business day
        response = 0

    return render(request, 'hw3/EOD.html')

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
    success=''
    if request.method == 'POST':
        first=request.POST['firstname']
        last=request.POST['lastname']
        comp=request.POST['company']

        new = Clients(first_name = first, last_name= last, company = comp)
        new.save()
        success = 'Success!'

    return render(request,'hw3/newTrader.html', context= {'success': success})

def addtrade(request):
    """
    API interface: Request handler for adding a new trade to :model:`hw1.Trades`.

    Required parameters:

        1. First name of the trader
        2. Last name of the trader
        3. Company the trader belongs to

    """
    if request.method == 'POST':
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
        new = Trade(status = 0, time = date_time, product_code = product, month_code = month, year = year, lots = lots, buy_or_sell = sign, order_type = type, price = price, trader = trader)
        post_data = {'id': id, 'type': type, 'side': side, 'symbol': product, 'price': price, 'lots' : lots}
        requests.post('localhost:8080/fix/process-order', data=post_data)
        new.save()
        return HttpResponseRedirect('/hw3/?success=true')
    else:
       return render(request, 'hw3/newTrade.html')

def exchange_message(request):
    if request.method == 'POST':
        orderStatus = request.POST.get('OrderStatus', False)
        for key, value in request.POST.iteritems():
            print key + ": " + value + "\n"
        if orderStatus == "partial fill":
            tradeid = request.POST.get('ClOrdId', False)
            trade = Trade.objects.get(id=tradeid)
            trade.status = 4
            trade.save();
            lots = request.POST.get('LastShares', False)
            filled_price = request.POST.get('LastPrice', False)
            filled_id = request.POST.get('ExecID', False);
            filled_time = request.POST.get('TransactionTime', False)
            new = Portfolio(trade_id =  tradeid, lots = lots, filled_price = filled_price, filled_id  = filled_id, filled_time = filled_time)
        elif orderStatus == "complete fill":
            tradeid = request.POST.get('ClOrdId', False)
            trade = Trade.objects.get(id=tradeid)
            trade.status = 5;
            trade.save();
            lots = request.POST.get('LastShares', False)
            filled_price = request.POST.get('LastPrice', False)
            filled_id = request.POST.get('ExecID', False) 
            filled_time = request.POST.get('TransactionTime', False)
            new = Portfolio(trade_id =  tradeid, lots =  lots, filled_price = filled_price, filled_id = filled_id, filled_time = filled_time) 
        elif orderStatus == "ack":
            tradeid = request.POST.get('id', False)
            trade = Trade.objects.get(id=tradeid)
            trade.status = 3;
            trade.save();

def fixAck(request):
    tradeid = request.POST.get('id', False)
    trade = Trade.objects.get(id=tradeid)
    trade.status = 2;
    trade.save();

def aggregate(request):
    """
    API interface: Request handler for getting the aggregate position of a single trader, or the overall aggregate position from :model:`hw1.Trades`.

        Required parameters: Trader_ID (unique ID or a blank field)

    """
    if request.method == 'POST':
        traderid=request.POST['traderid']
        cursor=connection.cursor()
        if (traderid == ""):
            cursor.execute("select td.trader as trader_id, max(cl.first_name) as `First Name`, max(cl.last_name) as `Last Name`, concat(td.`product_code`,td.`month_code`,td.year) as product, sum(pt.lots*td.`buy_or_sell`) as `Aggregate Position`, max(mp.`price`) as market_price, sum(pt.`filled_price`*pt.lots*td.`buy_or_sell`) as `Aggregate Purchase Cost`, sum(pt.lots*td.`buy_or_sell`)*max(mp.price) as `Asset Net Worth` from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id group by trader_id, product")
            header=['Trade_ID','First_Name','Last_Name','Product','Aggregate_Position','Market_Price','Aggregate_Purchase_Cost','Asset_Net_Worth']
        else:
            cursor.execute("select td.trader as trader_id, max(cl.first_name) as `First Name`, max(cl.last_name) as `Last Name`, concat(td.`product_code`,td.`month_code`,td.year) as product, sum(pt.lots*td.`buy_or_sell`) as `Aggregate Position`, max(mp.`price`) as market_price, sum(pt.`filled_price`*pt.lots*td.`buy_or_sell`) as `Aggregate Purchase Cost`, sum(pt.lots*td.`buy_or_sell`)*max(mp.price) as `Asset Net Worth` from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id where td.trader=%s group by trader_id, product",[traderid])
            header=['Trade_ID','First_Name','Last_Name','Product','Aggregate_Position','Market_Price','Aggregate_Purchase_Cost','Asset_Net_Worth']

        aggregate_position = cursor.fetchall()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="aggregate.csv"'
        writer = csv.writer(response)
        writer.writerow(header)
        for i in range(len(aggregate_position)):
            writer.writerow(aggregate_position[i])

        return response
    
    return render(request, 'hw3/aggregate.html')

def aggregateSwaps(request):
    if request.method == 'POST':
        traderid=request.POST['traderid']
        cursor=connection.cursor()
        
        if traderid == "":
            cursor.execute("select * from Swaps")
        else:
            cursor.execute("select * from Swaps where TraderID=%s",[traderid])

        header=['Swap_ID','Start Date','Termination date','Fixed Rate','Float Rate','Float Spread','Notional','Who Pays Fixed','Clearing House','Trader']
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
    if request.method == 'POST':
        traderid=request.POST['traderid']
        cursor=connection.cursor()
        if (traderid == ""):
            cursor.execute("select td.trader as trader_id, cl.first_name, cl.last_name, concat(td.`product_code`,td.`month_code`,td.year) as product,pt.filled_time,td.`buy_or_sell`, pt.lots,pt.`filled_price`,mp.`price` as market_price from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id;")
            header=['Trade_ID','First_Name','Last_Name','Product','Filled_Time','Buy(+1)/Sell(-1)','Lots','Filled_Price (in cents)','Market_Price']
        else:
            cursor.execute("select td.trader as trader_id, cl.first_name, cl.last_name, concat(td.`product_code`,td.`month_code`,td.year) as product,pt.filled_time,td.`buy_or_sell`, pt.lots,pt.`filled_price`,mp.`price` as market_price from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id where td.trader= %s",[traderid])
            header=['Trade_ID','First_Name','Last_Name','Product','Filled_Time','Buy(+1)/Sell(-1)','Lots','Filled_Price (in cents)','Market_Price']
        aggregate_position = cursor.fetchall()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachement; filename="history.csv"'
        writer = csv.writer(response)
        writer.writerow(header)
        for i in range(len(aggregate_position)):
            writer.writerow(aggregate_position[i]);

        return response
    
    return render(request, 'hw3/history.html')

def pnl(request):
    """
    API interface: Request handler for getting the trade history of a single trader, or all trade histories from :model:`hw1.Trades`.

        Required parameters: Trader_ID (unique ID or a blank field)

    """
    if request.method == 'POST':
        traderid=request.POST['traderid']
        cursor=connection.cursor()
        if (traderid == ""):
            cursor.execute("select td.trader as trader_id, cl.first_name, cl.last_name, concat(td.`product_code`,td.`month_code`,td.year) as product,pt.filled_time,td.`buy_or_sell`, pt.lots,pt.`filled_price`,mp.`price` as market_price, (mp.`price`-pt.`filled_price`)*td.`buy_or_sell` as `PnL per lot`, (mp.`price`-pt.`filled_price`)*`buy_or_sell`*pt.lots as `PnL per Trade` from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id")
            header=['Trade_ID','First_Name','Last_Name','Product','Filled_Time','Buy(+1)/Sell(-1)','Lots','Filled_Price (in cents)','Market_Price','PnL_per_Lot','PnL_per_Trade']
        else:
            cursor.execute("select td.trader as trader_id, cl.first_name, cl.last_name, concat(td.`product_code`,td.`month_code`,td.year) as product,pt.filled_time,td.`buy_or_sell`, pt.lots,pt.`filled_price`,mp.`price` as market_price, (mp.`price`-pt.`filled_price`)*td.`buy_or_sell` as `PnL per lot`, (mp.`price`-pt.`filled_price`)*`buy_or_sell`*pt.lots as `PnL per Trade` from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id where td.trader=%s",[traderid])
            header=['Trade_ID','First_Name','Last_Name','Product','Filled_Time','Buy(+1)/Sell(-1)','Lots','Filled_Price (in cents)','Market_Price','PnL_per_Lot','PnL_per_Trade']
        aggregate_position = cursor.fetchall()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachement; filename="pnl.csv"'
        writer = csv.writer(response)
        writer.writerow(header)
        for i in range(len(aggregate_position)):
            writer.writerow(aggregate_position[i]);

        return response

    return render(request, 'hw3/pnl.html')

def portfolio(request):
    """
    API interface: Request handler for getting the trade history of a single trader, or all trade histories from :model:`hw1.Trades`.

        Required parameters: Trader_ID (unique ID or a blank field)

    """
    if request.method == 'POST':
        traderid=request.POST['traderid']
        cursor=connection.cursor()
        if (traderid == ""):
            cursor.execute("select td.trader as trader_id, cl.first_name, cl.last_name, concat(td.`product_code`,td.`month_code`,td.year) as product,td.`buy_or_sell`, pt.lots,pt.`filled_price`,mp.`price` as market_price from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id")
            header=['Trade_ID','First_Name','Last_Name','Product','Buy_or_Sell','Lots','Filled_Price (in cents)', 'Market_Price']
        else:
            cursor.execute("select td.trader as trader_id, cl.first_name, cl.last_name, concat(td.`product_code`,td.`month_code`,td.year) as product,td.`buy_or_sell`, pt.lots,pt.`filled_price`,mp.`price` as market_price from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id where td.trader= %s",[traderid])
            header=['Trade_ID','First_Name','Last_Name','Product','Buy_or_Sell','Lots','Filled_Price (in cents)', 'Market_Price']
        aggregate_position = cursor.fetchall()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachement; filename="portfolio.csv"'
        writer = csv.writer(response)
        writer.writerow(header)
        for i in range(len(aggregate_position)):
            writer.writerow(aggregate_position[i]);

        return response

    return render(request, 'hw3/portfolio.html')

def pnlbytrade(request):
    """
    API interface: Request handler for getting the trade history of a single trader, or all trade histories from :model:`hw1.Trades`.

        Required parameters: Trader_ID (unique ID or a blank field)

    """
    if request.method == 'POST':
        traderid=request.POST['traderid']
        cursor=connection.cursor()
        if (traderid == ""):
            cursor.execute("select td.trader as trader_id, cl.first_name, cl.last_name, concat(td.`product_code`,td.`month_code`,td.year) as product,td.`buy_or_sell`, pt.lots,pt.`filled_price`,mp.`price` as market_price, (mp.`price`-pt.`filled_price`)*(case td.`buy_or_sell` when 1 then 1 else -1 end) as `PnL per lot`, (mp.`price`-pt.`filled_price`)*(case td.`buy_or_sell` when 1 then 1 else -1 end)*pt.lots as `PnL per Trade` from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id")
            header=['Trade_ID','First_Name','Last_Name','Product','Buy_or_Sell','Lots','Filled_Price (in cents)', 'Market_Price', 'PnL_per_Lot','PnL_per_Trade']
        else:
            cursor.execute("select td.trader as trader_id, cl.first_name, cl.last_name, concat(td.`product_code`,td.`month_code`,td.year) as product,td.`buy_or_sell`, pt.lots,pt.`filled_price`,mp.`price` as market_price, (mp.`price`-pt.`filled_price`)*(case td.`buy_or_sell` when 1 then 1 else -1 end) as `PnL per lot`, (mp.`price`-pt.`filled_price`)*(case td.`buy_or_sell` when 1 then 1 else -1 end)*pt.lots as `PnL per Trade` from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id where td.trader= %s",[traderid])
            header=['Trade_ID','First_Name','Last_Name','Product','Buy_or_Sell','Lots','Filled_Price (in cents)', 'Market_Price','PnL_per_Lot','PnL_per_Trade']
        aggregate_position = cursor.fetchall()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachement; filename="pnlbytrade.csv"'
        writer = csv.writer(response)
        writer.writerow(header)
        for i in range(len(aggregate_position)):
            writer.writerow(aggregate_position[i])

        return response

    return render(request, 'hw3/pnlbytrade.html')

def pnlbytrader(request):
    """
    API interface: Request handler for getting the trade history of a single trader, or all trade histories from :model:`hw1.Trades`.

        Required parameters: Trader_ID (unique ID or a blank field)

    """
    if request.method == 'POST':
        traderid=request.POST['traderid']
        cursor=connection.cursor()
        if (traderid == ""):
            cursor.execute("select td.trader as trader_id, max(cl.first_name) as `First Name`, max(cl.last_name) as `Last Name`, sum((mp.`price`-pt.`filled_price`)*(case td.`buy_or_sell` when 1 then 1 else -1 end)*pt.lots) as `PnL for Trader` from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id group by td.trader")
            header=['Trade_ID','First_Name','Last_Name','PnL_for_Trader']
        else:
            cursor.execute("select td.trader as trader_id, max(cl.first_name) as `First Name`, max(cl.last_name) as `Last Name`, sum((mp.`price`-pt.`filled_price`)*(case td.`buy_or_sell` when 1 then 1 else -1 end)*pt.lots) as `PnL for Trader` from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id where td.trader= %s group by td.trader",[traderid])
            header=['Trade_ID','First_Name','Last_Name','PnL_for_Trader']
        aggregate_position = cursor.fetchall()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachement; filename="pnlbytrader.csv"'
        writer = csv.writer(response)
        writer.writerow(header)
        for i in range(len(aggregate_position)):
            writer.writerow(aggregate_position[i]);

        return response

    return render(request, 'hw3/pnlbytrader.html')

def pnlbyproduct(request):
    """
    API interface: Request handler for getting the trade history of a single trader, or all trade histories from :model:`hw1.Trades`.

        Required parameters: Trader_ID (unique ID or a blank field)

    """
    if request.method == 'POST':
        traderid=request.POST['traderid']
        cursor=connection.cursor()
        if (traderid == ""):
            cursor.execute("select td.trader as trader_id, max(cl.first_name) as `First Name`, max(cl.last_name) as `Last Name`, concat(td.`product_code`,td.`month_code`,td.year) as product,td.`buy_or_sell`, sum(pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) as `Aggregate Position`,(case sum(pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) when 0 then 0 else sum(pt.`filled_price`*pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) end)/sum(pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) as `Average Holding Price`,max(mp.`price`) as market_price, (case sum(pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) when 0 then 0 else sum((mp.`price`-pt.`filled_price`)*pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end))/sum(pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end))  end) as `PnL per lot`, sum((mp.`price`-pt.`filled_price`)*pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) as `PnL per Trade` from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id group by trader_id, product")
            header=['Trade_ID','First_Name','Last_Name','Product','Buy_or_Sell','Aggregate_Position','Average_Holding_Price', 'Market_Price','PnL_per_Lot','PnL_per_Product']
        else:
            cursor.execute("select td.trader as trader_id, max(cl.first_name) as `First Name`, max(cl.last_name) as `Last Name`, concat(td.`product_code`,td.`month_code`,td.year) as product,td.`buy_or_sell`, sum(pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) as `Aggregate Position`,(case sum(pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) when 0 then 0 else sum(pt.`filled_price`*pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) end)/sum(pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) as `Average Holding Price`,max(mp.`price`) as market_price, (case sum(pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) when 0 then 0 else sum((mp.`price`-pt.`filled_price`)*pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end))/sum(pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end))  end) as `PnL per lot`, sum((mp.`price`-pt.`filled_price`)*pt.lots*(case td.`buy_or_sell` when 1 then 1 else -1 end)) as `PnL per Trade` from portfolio as pt left join trade as td on pt.trade_id = td.id left join market_price as mp on td.product_code = mp.`product_code` and td.month_code = mp.month and td.year = mp.year left join clients as cl on td.trader=cl.id where td.trader= %s group by trader_id, product",[traderid])
            header=['Trade_ID','First_Name','Last_Name','Product','Buy_or_Sell','Aggregate_Position','Average_Holding_Price', 'Market_Price','PnL_per_Lot','PnL_per_Product']
        aggregate_position = cursor.fetchall()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachement; filename="pnlbyproduct.csv"'
        writer = csv.writer(response)
        writer.writerow(header)
        for i in range(len(aggregate_position)):
            writer.writerow(aggregate_position[i]);

        return response

    return render(request, 'hw3/pnlbyproduct.html')
