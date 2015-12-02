from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Clients, Trade, Portfolio
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

        return render(request, 'hw3/?success=true')

    return render(request, 'hw3/addSwap.html')

def EODProcess(request):
    if request.method == 'POST':
        #TODO: Query database for aggregate, and roll day to the next

        #TODO: Figure out a way to store the calendar, and find the next business day
        response = 0

    return render(request, 'hw3/EOD.html')
