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
import decimal
from django.utils.timezone import is_aware
from .models import *
import json
import re
import random


# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')

def voice(request):
    return render(request, 'voice.html')

var3 =None
def Flightview(request):
    username = request.GET.get('username', '')
    global var3
    def var3():
        return username
    destination = var1()
    date_start= var2()
    boarding_date = reFormatDateMMDDYYYY(date_start)
    flight = list(Flight.objects.filter(destination = destination)
    .filter(boarding_date = boarding_date)
    .values('flight_id','departure','gate','boarding_time','boarding_date'))
    flight_class = list(Flightclass.objects.all().values().order_by('price'))
    data = dict()
    data['flight'] = flight
    data['flight_class'] = flight_class
    data['destination'] = destination
    return render(request, 'flight.html', data)

def ticket(request):
    ticket_id = request.GET.get('ticket_id', '')
    ticket = list(Ticket.objects.filter(ticket_id=ticket_id)
    .values('ticket_id','flightid','flight_class','username','seat','flightid__departure','flightid__destination','flightid__gate','flightid__boarding_time'))
    data = dict()
    data['ticket'] = ticket
    return render(request, 'ticket.html', data)


class CustomerDetail(View):
    def get(self, request,username):
        customer = list(Customer.objects.filter(username=username).values('username','password'))
        if customer == []:
            data = dict()
            data['error'] = "Error!"
        else:
            data = dict()
            data['customer'] = customer
        return JsonResponse(data)

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


@method_decorator(csrf_exempt, name='dispatch')
class CustomersSignup(View):
    
    @transaction.atomic
    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            data = dict()
            data['result'] = form.errors
            return JsonResponse(data)


var1 = None
var2 = None
@method_decorator(csrf_exempt, name='dispatch')
class SearchTicket(View):
    
    @transaction.atomic
    def post(self, request):
        destination = request.POST['destination']
        date_start = request.POST['date_start']
        global var1
        global var2
        def var1():
            return destination
        def var2():
            return date_start
        data ={}
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class CreateTicket(View):
    
    @transaction.atomic
    def post(self, request):
        if Ticket.objects.count() != 0:        
            ticket_id_max = Ticket.objects.aggregate(Max('ticket_id'))['ticket_id__max']    
            ticket_id_temp = [re.findall(r'(\w+?)(\d+)', ticket_id_max)[0]][0]                
            next_ticket_id = ticket_id_temp[0] + str(int(ticket_id_temp[1])+1)        
        else:
            next_ticket_id = 'TK100000'
        print(next_ticket_id)
        user=var3() 
        Flightid = request.POST.get('flightid')
        Flightclass = request.POST.get('flight_class')
        dict_data = dict()
        dict_data['flightid'] = Flightid
        dict_data['flight_class'] = Flightclass
        dict_data['ticket_id'] = next_ticket_id
        dict_data['username'] = user
        dict_data['seat'] = random.randint(1, 200)
        
        data = dict()
        form = TicketForm(dict_data)
        if form.is_valid():

            form.save()
            data['ticket_id'] = next_ticket_id
        else:
            data['error'] = "Error!"
        return JsonResponse(data)


def reFormatDateMMDDYYYY(yyyymmdd):
        if (yyyymmdd == ''):
            return ''
        return  yyyymmdd[6:] + "-" + yyyymmdd[:2] + "-" + yyyymmdd[3:5]




