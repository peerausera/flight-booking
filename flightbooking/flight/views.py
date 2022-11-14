from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.db.models import Max
from django.db import transaction
from .models import *
import json
import re


# Create your views here.
    
def index(request):
    data = {}
    return render(request, 'index.html', data)

def login(request):
    data = {}
    return render(request, 'login.html', data)

def Customer(request):
    
    dataReport = dict()
    data = list(Customer.objects.all().values())
    columns = ("username", "password", "firstname", "birthday", "phonenumber")
    dataReport['column_name'] = columns
    dataReport['data'] = data

    return render(request, 'report_list_all_customer.html', dataReport)

def Flightclass(request):
    
    dataReport = dict()
    data = list(Flightclass.objects.all().values())
    columns = ("flight_class", "price")
    dataReport['column_name'] = columns
    dataReport['data'] = data

    return render(request, 'report_list_all_Flightclass.html', dataReport)

def Flight(request):
    
    dataReport = dict()
#    data = list(Flight.objects.all().values())
#    columns = ("flight_id","departure","destination","gate","boarding_time","boarding_date","flightclass","flightprice")
#    dataReport['column_name'] = columns
#    dataReport['data'] = data

    return render(request, 'flight.html', dataReport)

def Ticket(request):
    
    dataReport = dict()
#    data = list(Ticket.objects.all().values())
#    columns = ("Ticket_id", "flightclass", "buy_time", "seat", "count_ticket_left")
#    dataReport['column_name'] = columns
#    dataReport['data'] = data

    return render(request, 'ticket.html', dataReport)


