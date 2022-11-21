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
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')



def Flightview(request):

    # dataReport = dict()
#    data = list(Flight.objects.all().values())
#    columns = ("flight_id","departure","destination","gate","boarding_time","boarding_date","flightclass","flightprice")
#    dataReport['column_name'] = columns
#    dataReport['data'] = data
    username = request.GET.get('username', '')
    ticket = list(Ticket.objects.filter(username=username)
    .values('ticket_id','flightid','flight_class','username','seat','flightid__departure','flightid__destination','flightid__gate','flightid__boarding_time'))
    data = dict()
    data['ticket'] = ticket
    # print(data)
    return render(request, 'flight.html', data)


# def Ticket(request):

#     ticket = list(Ticket.objects.all().values())
#     data = dict()
#     data['customers'] = ticket

#     return render(request, 'ticket.html', data)
def ticket(request):
    username = request.GET.get('username', '')
    ticket = list(Ticket.objects.filter(username=username)
    .values('ticket_id','flightid','flight_class','username','seat','flightid__departure','flightid__destination','flightid__gate','flightid__boarding_time'))
    data = dict()
    data['ticket'] = ticket
    # print(data)
    return render(request, 'ticket.html', data)

# class getticket(View):
#     def post(self, request):
        
#         username = request.GET.get('username', '')
#         ticket = list(Ticket.objects.filter(username=username)
#         .values('ticket_id','flightid','flight_class','username','seat','flightid__departure','flightid__destination','flightid__gate','flightid__boarding_time'))
#         data = dict()
#         data['ticket'] = ticket
#         print(data)
#         return render(request, 'ticket.html', data)

# class Ticketview(View):
#     def get(self, request):
#         ticket = list(Ticket.objects.all().values())
#         data = dict()
#         data['ticket'] = ticket

#         return render(request, 'ticket.html', data)

class CustomerDetail(View):
    def get(self, request,username):
        customer = list(Customer.objects.filter(username=username).values('username','password'))
        if customer == []:
            data = dict()
            data['error'] = "Error!"
        else:
            data = dict()
            data['customer'] = customer
            print(data)
        return JsonResponse(data)

# class TicketForm(forms.ModelForm):
#     class Meta:
#         model = Ticket
#         fields = '__all__'

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
        # print(request.POST)
        destination = request.POST['destination']
        date_start = request.POST['date_start']
        global var1,var2
        def var1():
            return destination
        def var2():
            return date_start
        # print(date_start)
        # print(destination)
        # form = TicketForm(request.POST)
        # if form.is_valid():
        #     form.save()
        # else:
        #     data = dict()
        #     data['result'] = form.errors
        data ={}
        return JsonResponse(data)