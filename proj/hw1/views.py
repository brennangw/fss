from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .models import Clients, Trades

# Create your views here.

def index(request):
    return render(request, 'hw1/index.html')

def addtrader(request):
    first=request.POST['firstname']
    last=request.POST['lastname']
    comp=request.POST['company']

    new = Clients(first_name = first, last_name= last, company = comp)
    new.save()

    return render(request, 'hw1/index.html')

def addtrade(request):
    return render(request, 'hw1/index.html')

def aggregate(request):
    return render(request, 'hw1/index.html')