from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Max
from django.db import transaction
from gTTS.templatetags.gTTS import say
from .models import *
import re
import random


# Create your views here.

# Index page
def index(request):
    return render(request, 'index.html')

# Login page
def login(request):
    disabled = request.GET.get('disabled', '')                          # Get disable data
    data = dict()
    data['disabled'] = disabled
    # Check if user is disabled
    if disabled == 'true':
        obj = say(language='th', text="ลงชื่อเข้าใช้โดยใช้ชื่อผู้ใช้และรหัสผ่าน จากนั้นกดปุ่มลงชื่อเข้าใช้สีแดง ....หากยังไม่เคยสมัครใช้บริการ กดปุ่มสมัครเลยทางขวา")
        data['obj'] = obj
    return render(request, 'login.html',data)

# Set global variable to None
var3 =None

# Flight page
def Flightview(request):
    username = request.GET.get('username', '')                          # Get username
    global var3                                                         # Craete global variable
    def var3(): 
        return username 
    destination = var1()                                                # Get data from global variable
    date_start= var2()                                                  # Get data from global variable
    boarding_date = reFormatDateMMDDYYYY(date_start)                    # Reformat date to yyyy/mm/dd
    # Get data from database
    flight = list(Flight.objects.filter(destination = destination)  
    .filter(boarding_date = boarding_date)
    .values('flight_id','departure','gate','boarding_time','boarding_date'))
    flight_class = list(Flightclass.objects.all().values().order_by('price'))
    Customer_disabled = Customer.objects.filter(username = username).values('disabled')             # Get disabled data from database
    disabled= ' '.join(str(item['disabled']) for item in Customer_disabled)                         # change foemat to string
    data = dict()
    data['flight'] = flight
    data['flight_class'] = flight_class
    data['destination'] = destination
    print(disabled)
    # Check if user is disabled
    if disabled == 'True':
        say_text = "ผลการค้นหาพบเที่ยวบินจำนวน " + str(len(data['flight'])) + " เที่ยวบิน ... class ของเที่ยวบินให้เลือกได้แก่ economy business และ first class เรียงตามลำดับ .... สามารถกดปุ่มเลือกเที่ยวบินเพื่อจองตั๋ว "
        obj = say(language='th', text=say_text)                         # Text to speech
        data['obj'] = obj
    return render(request, 'flight.html', data)

# Ticket page
def ticket(request):
    ticket_id = request.GET.get('ticket_id', '')                        # Get ticket id
    # Get data from database
    ticket = list(Ticket.objects.filter(ticket_id=ticket_id)
    .values('ticket_id','flightid','flight_class','username','seat','flightid__departure','flightid__destination','flightid__gate','flightid__boarding_time'))
    data = dict()
    data['ticket'] = ticket
    username = var3()
    Customer_disabled = Customer.objects.filter(username = username).values('disabled')             # Get disabled data from database
    disabled= ' '.join(str(item['disabled']) for item in Customer_disabled)                         # change format to string
    phone_number = Customer.objects.filter(username = username).values('phonenumber')               # Get phonenumber data from database
    phone = ' '.join(str(item['phonenumber']) for item in phone_number)                             # change format to string
    # Check if user is disabled
    if disabled == 'True':
        say_text = "เจ้าหน้าที่จะทำการติดต่อเพื่อยืนยันการจองตั๋ว เบอร์โทรศัพท์" + phone + "....... หากเกิดปัญหาหรือมีข้อสงสัยสามารถโทรหา call center เบอร์โทรศัพท์ 0123456789 "
        obj = say(language='th', text=say_text)                         # Text to speech
        data['obj'] = obj
    return render(request, 'ticket.html', data)

# Ajax get username and password from database
class CustomerDetail(View):
    def get(self, request,username):
        # Get data from database
        customer = list(Customer.objects.filter(username=username).values('username','password'))
        # Check if user not exit
        if customer == []:
            data = dict()
            data['error'] = "Error!"
        else:
            data = dict()
            data['customer'] = customer
        return JsonResponse(data)

# Form from model
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

# Save user to customer database
@method_decorator(csrf_exempt, name='dispatch')
class CustomersSignup(View):
    
    @transaction.atomic
    def post(self, request):
        form = CustomerForm(request.POST)                               # Get data from ajax
        if form.is_valid():                                             # Check valid
            form.save()
        else:
            data = dict()
            data['result'] = form.errors
            return JsonResponse(data)

# Set global variable to None
var1 = None
var2 = None

# Save data from index to global varible
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

# Create ticket
@method_decorator(csrf_exempt, name='dispatch')
class CreateTicket(View):
    
    @transaction.atomic
    def post(self, request):
        #create ticket id 
        if Ticket.objects.count() != 0:                                                         # Check if have ticket in ticket database      
            ticket_id_max = Ticket.objects.aggregate(Max('ticket_id'))['ticket_id__max']        # SELECT MAX(ticket_id) FROM ticket
            ticket_id_temp = [re.findall(r'(\w+?)(\d+)', ticket_id_max)[0]][0]                  # Split 'TK100000' to 'TK' , '100000'
            next_ticket_id = ticket_id_temp[0] + str(int(ticket_id_temp[1])+1)                  # next_ticket_id = 'TK' + '100001' = 'TK100000'
        else:
            next_ticket_id = 'TK100000'
        print('New ticket id is ' + next_ticket_id)
        user=var3()                                                                             # Get username from global variable
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
        # Save form
        if form.is_valid():                                                                     

            form.save()
            data['ticket_id'] = next_ticket_id
        else:
            data['error'] = "Error!"
        return JsonResponse(data)



# Reformat date to yyyy/mm/dd
def reFormatDateMMDDYYYY(yyyymmdd):
        # If format correct, not reformat
        if (yyyymmdd == ''):
            return ''
        return  yyyymmdd[6:] + "-" + yyyymmdd[:2] + "-" + yyyymmdd[3:5]






