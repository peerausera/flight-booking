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


def ListAllTicket(request):
    return render(request, 'list_all_ticket.html')

class TicketList(View):
    def get(self, request):
        ticket = list(Ticket.objects.all().values())
        data = dict()
        data['data'] = ticket
        
        return JsonResponse(data)


def getTicket(request):
    ticket_id = request.GET.get('ticket_id', '')
    ticket = list(Ticket.objects.filter(ticket_id=ticket_id).values())
    data = dict()
    data['ticket'] = ticket
    
    return render(request, 'list_all_ticket.html', data)

class TicketGet(View):
    def get(self, request, ticket_id):
        ticket = list(Ticket.objects.filter(ticket_id=ticket_id).values())
        data = dict()
        data['ticket'] = ticket
        print(data)
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class TicketDelete(View):
    def post(self, request):

        ticket_id = request.POST['ticket_id']
        ticket = Ticket.objects.get(ticket_id=ticket_id)
        data = dict()
        if ticket:
            ticket.delete()
            data['message'] = "Ticket Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        ticket = list(Ticket.objects.all().values())
        data['ticket'] = ticket

        return JsonResponse(data)

def ListAllCustomer(request):
    return render(request, 'list_all_customer.html')

class CustomerList(View):
    def get(self, request):
        customers = list(Customer.objects.all().values('username','firstname','lastname','birthday','phonenumber'))
        data = dict()
        data['customers'] = customers
        return JsonResponse(data)


def getCustomer(request):
    username = request.GET.get('username', '')
    customers = list(Customer.objects.filter(username=username).values('username','firstname','lastname','birthday','phonenumber'))
    data = dict()
    data['data'] = customers

    return render(request, 'list_all_customer.html', data)

class CustomerGet(View):
    def get(self, request, username):
        customers = list(Customer.objects.filter(username=username).values('username','firstname','lastname','birthday','phonenumber'))
        data = dict()
        data['data'] = customers

        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class CustomerDelete(View):
    def post(self, request):

        username = request.POST['username']
        customer = Customer.objects.get(username=username)
        data = dict()
        if customer:
            customer.delete()
            data['message'] = "Customer Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        customers = list(Customer.objects.all().values('username','firstname','lastname','birthday','phonenumber'))
        data['customers'] = customers

        return JsonResponse(data)


def ReportListAllFlight(request):
    dataReport = dict()
    data = list(Flight.objects.all())
    columns = ('flight_id','departure','destination','gate','boarding_time','boarding_date')
    print(data)
    dataReport['column_name']= columns
    dataReport['data']=data
    return render(request, 'report_list_all_flight.html',dataReport)

def FMindex(request):
    data = {}
    return render(request, 'flightmanahement.html', data)

# @method_decorator(csrf_exempt, name='dispatch')
# class Flightsave(View):
    
#     @transaction.atomic
#     def post(self, request):
#         print(request.POST)
#         data = dict()
#         form = FlightForm(request.POST)
#         if form.is_valid():
#             flight = form.save()
#             print(model_to_dict(flight))
#             data['flight'] = model_to_dict(flight)
#         else:
#             data['result'] = form.errors
#         return JsonResponse(data)


# class ProductList(View):
#     def get(self, request):
#         products = list(Product.objects.all().values())
#         data = dict()
#         data['products'] = products

#         return JsonResponse(data)

# class CustomerList(View):
#     def get(self, request):
#         customers = list(Customer.objects.all().values())
#         data = dict()
#         data['customers'] = customers

#         return JsonResponse(data)

# class CustomerDetail(View):
#     def get(self, request, customer_code):
#         customer = list(Customer.objects.filter(customer_code=customer_code).values())
#         data = dict()
#         data['customers'] = customer

#         return JsonResponse(data)

# class InvoiceList(View):
#     def get(self, request):
#         invoices = list(Invoice.objects.order_by('invoice_no').all().values())
#         data = dict()
#         data['invoices'] = invoices

#         return JsonResponse(data)

# class InvoiceDetail(View):
#     def get(self, request, pk, pk2):

#         invoice_no = pk + '/' + pk2

#         invoice = list(Invoice.objects.select_related('customer_code')
#             .filter(invoice_no=invoice_no)
#             .values('invoice_no', 'date', 'customer_code', 'customer_code__name', 'due_date'
#             , 'total', 'vat', 'amount_due'))
#         invoicelineitem = list(InvoiceLineItem.objects.select_related('product_code')
#             .filter(invoice_no=invoice_no)
#             .values('invoice_no', 'item_no', 'product_code', 'product_code__name', 'product_code__units'
#             , 'quantity', 'product_total'))

#         data = dict()
#         data['invoice'] = invoice
#         data['invoicelineitem'] = invoicelineitem

#         return JsonResponse(data)

# class InvoiceForm(forms.ModelForm):
#     class Meta:
#         model = Invoice
#         fields = '__all__'

# class LineItemForm(forms.ModelForm):
#     class Meta:
#         model = InvoiceLineItem
#         fields = '__all__'

# @method_decorator(csrf_exempt, name='dispatch')
# class InvoiceCreate(View):

#     @transaction.atomic
#     def post(self, request):
#         if Invoice.objects.count() != 0:        # Check Number of Record of Invoice Table == SELECT COUNT(*) FROM invoice
#             invoice_no_max = Invoice.objects.aggregate(Max('invoice_no'))['invoice_no__max']    # SELECT MAX(invoice_no) FROM invoice
#             invoice_no_temp = [re.findall(r'(\w+?)(\d+)', invoice_no_max)[0]][0]                # Split 'IN100/22' to 'IN' , '100'
#             next_invoice_no = invoice_no_temp[0] + str(int(invoice_no_temp[1])+1) + "/22"       # next_invoice_no = 'IN' + '101' + '/22' = 'IN101/22'
#         else:
#             next_invoice_no = "IN100/22"        # If Number of Record of Invoice = 0 , next_invoice_no = IN100/22
#         print(next_invoice_no)
#         # Copy POST data and correct data type Ex 1,000.00 -> 1000.00
#         request.POST = request.POST.copy()
#         request.POST['invoice_no'] = next_invoice_no
#         request.POST['date'] = reFormatDateMMDDYYYY(request.POST['date'])
#         request.POST['due_date'] = reFormatDateMMDDYYYY(request.POST['due_date'])
#         request.POST['total'] = reFormatNumber(request.POST['total'])
#         request.POST['vat'] = reFormatNumber(request.POST['vat'])
#         request.POST['amount_due'] = reFormatNumber(request.POST['amount_due'])
        
#         data = dict()
#         # Insert correct data to invoice
#         form = InvoiceForm(request.POST)
        
#         if form.is_valid():
#             invoice = form.save()
            
#             # Delete all invoice_line_item of invoice_no before loop insert new data
#             InvoiceLineItem.objects.filter(invoice_no=next_invoice_no).delete()

#             # Read lineitem from ajax and convert to json dictionary
#             dict_lineitem = json.loads(request.POST['lineitem'])
#             # Loop replace json data with correct data type Ex 1,000.00 -> 1000.00
#             for lineitem in dict_lineitem['lineitem']:
#                 lineitem['invoice_no'] = next_invoice_no
#                 lineitem['unit_price'] = reFormatNumber(lineitem['unit_price'])
#                 lineitem['quantity'] = reFormatNumber(lineitem['quantity'])
#                 lineitem['product_total'] = reFormatNumber(lineitem['extended_price'])
    
#                 # Insert correct data to invoice_line_item
#                 formlineitem = LineItemForm(lineitem)
#                 print (formlineitem)
#                 try:
#                     formlineitem.save()
                    
#                 except :
#                     # Check something error to show and rollback transaction both invoice and invoice_line_item table
#                     data['error'] = formlineitem.errors
#                     print (formlineitem.errors)
#                     transaction.set_rollback(True)

#             # if insert invoice and invoice_line_item success, return invoice data to caller
#             data['invoice'] = model_to_dict(invoice)
#         else:
#             # if invoice from is not valid return error message
#             data['error'] = form.errors
#             print (form.errors)

#         return JsonResponse(data)

# @method_decorator(csrf_exempt, name='dispatch')
# class InvoiceUpdate(View):

#     @transaction.atomic
#     def post(self, request):
#         # Get inovice_no from POST data
#         invoice_no = request.POST['invoice_no']

#         invoice = Invoice.objects.get(invoice_no=invoice_no)
#         request.POST = request.POST.copy()
#         request.POST['date'] = reFormatDateMMDDYYYY(request.POST['date'])
#         request.POST['due_date'] = reFormatDateMMDDYYYY(request.POST['due_date'])
#         request.POST['total'] = reFormatNumber(request.POST['total'])
#         request.POST['vat'] = reFormatNumber(request.POST['vat'])
#         request.POST['amount_due'] = reFormatNumber(request.POST['amount_due'])

#         data = dict()
#         # instance is object that will be udpated
#         form = InvoiceForm(instance=invoice, data=request.POST)
#         if form.is_valid():
#             invoice = form.save()

#             InvoiceLineItem.objects.filter(invoice_no=invoice_no).delete()

#             dict_lineitem = json.loads(request.POST['lineitem'])
#             for lineitem in dict_lineitem['lineitem']:
#                 lineitem['invoice_no'] = invoice_no
#                 lineitem['unit_price'] = reFormatNumber(lineitem['unit_price'])
#                 lineitem['quantity'] = reFormatNumber(lineitem['quantity'])
#                 lineitem['product_total'] = reFormatNumber(lineitem['extended_price'])
#                 formlineitem = LineItemForm(lineitem)
#                 if formlineitem.is_valid():
#                     formlineitem.save()
#                 else:
#                     data['error'] = form.errors
#                     transaction.set_rollback(True)

#             data['invoice'] = model_to_dict(invoice)
#         else:
#             data['error'] = form.errors
#             print (form.errors)

#         return JsonResponse(data)

# @method_decorator(csrf_exempt, name='dispatch')
# class InvoiceDelete(View):
#     def post(self, request):
#         invoice_no = request.POST["invoice_no"]

#         data = dict()
#         invoice = Invoice.objects.get(invoice_no=invoice_no)
#         if invoice:
#             invoice.delete()
#             InvoiceLineItem.objects.filter(invoice_no=invoice_no).delete()
#             data['message'] = "Invoice Deleted!"
#         else:
#             data['error'] = "Error!"

#         return JsonResponse(data)