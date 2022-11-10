from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import connection

from report.models import *
import json

# Create your views here.
def index(request):
    return render(request, 'forms_paymentmethod.html')

def customer(request):
    customer_code = request.GET.get('customer_code', '')
    customers = list(Customer.objects.filter(customer_code=customer_code).values())
    data = dict()
    data['customers'] = customers
    
    return render(request, 'forms_customer.html', data)

class ProductList(View):
    def get(self, request):
        products = list(Product.objects.all().values())
        data = dict()
        data['products'] = products

        return JsonResponse(data)


def payment(request):
    Paymentmethod = request.GET.get('payment_method', '')
    Payment_method = list(Payment.objects.filter(payment_method=Paymentmethod).values())
    data = dict()
    data['Paymentmethod'] = Payment_method
    
    return render(request, 'forms_paymentmethod.html', data)

class PaymentmethodList(View):
    def get(self, request):
        Payment_method = list(Payment.objects.all().values())
        data = dict()
        data['Paymentmethod'] = Payment_method

        return JsonResponse(data)

class PaymentmethodGet(View):
    def get(self, request, payment_method):
        Payment_method = list(Payment.objects.filter(payment_method=payment_method).values())
        data = dict()
        data['Paymentmethod'] = Payment_method

        return JsonResponse(data)       

@method_decorator(csrf_exempt, name='dispatch')
class PaymentmethodSave(View):
    def post(self, request):

        form = PaymentmethodForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            return JsonResponse(ret)

        Payment_method = list(Payment.objects.all().values())
        data = dict()
        data['Paymentmethod'] = Payment_method
        
        return render(request, 'forms_paymentmethod.html', data)

class PaymentmethodForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'


@method_decorator(csrf_exempt, name='dispatch')
class PaymentmethodSave2(View):
    def post(self, request):

        form = PaymentmethodForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            ret['Paymentmethod'] = list()
            return JsonResponse(ret)

        Payment_method = list(Payment.objects.all().values())
        data = dict()
        data['Paymentmethod'] = Payment_method

        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class PaymentmethodDelete(View):
    def post(self, request):

        payment_method = request.POST['payment_method']
        payment = Payment.objects.get(payment_method=payment_method)
        data = dict()
        if payment:
            payment.delete()
            data['message'] = "Payment Method Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        Payment_method = list(Payment.objects.all().values())
        data['Paymentmethod'] = Payment_method

        return JsonResponse(data)
        


class CustomerList(View):
    def get(self, request):
        customers = list(Customer.objects.all().values())
        data = dict()
        data['customers'] = customers

        return JsonResponse(data)

class CustomerGet(View):
    def get(self, request, customer_code):
        customers = list(Customer.objects.filter(customer_code=customer_code).values())
        data = dict()
        data['customers'] = customers

        return JsonResponse(data)        

@method_decorator(csrf_exempt, name='dispatch')
class CustomerSave(View):
    def post(self, request):

        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            return JsonResponse(ret)

        customers = list(Customer.objects.all().values())
        data = dict()
        data['customers'] = customers
        
        return render(request, 'forms_customer.html', data)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class CustomerSave2(View):
    def post(self, request):

        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            ret['customers'] = list()
            return JsonResponse(ret)

        customers = list(Customer.objects.all().values())
        data = dict()
        data['customers'] = customers

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class CustomerDelete(View):
    def post(self, request):

        customer_code = request.POST['customer_code']
        customer = Customer.objects.get(customer_code=customer_code)
        data = dict()
        if customer:
            customer.delete()
            data['message'] = "Customer Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        customers = list(Customer.objects.all().values())
        data['customers'] = customers

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

def ReportListAllProducts(request):
    
    dataReport = dict()
    data = list(Product.objects.all().values())
    columns = ("Code", "Name", "Units", "Product Type")
    dataReport['column_name'] = columns
    dataReport['data'] = data

    return render(request, 'report_list_all_products.html', dataReport)

def ReportListAllInvoices(request):
    cursor = connection.cursor()
    cursor.execute ('SELECT i.invoice_no as "Invoice No", i.date as "Date" '
                             ' , i.customer_code as "Customer Code", c.name as "Customer Name" '
                             ' , i.due_date as "Due Date", i.total as "Total", i.vat as "VAT", i.amount_due as "Amount Due" '
                             ' , ili.product_code as "Product Code", p.name as "Product Name" '
                             ' , ili.quantity as "Quantity", ili.unit_price as "Unit Price", ili.product_total as "Extended Price" '
                             ' FROM invoice i JOIN customer c ON i.customer_code = c.customer_code '
                             '  JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                             '  JOIN product p ON ili.product_code = p.code '
                             ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)

    return render(request, 'report_list_all_invoices.html', dataReport)

def ReportProductsSold(request):

    cursor = connection.cursor()
    cursor.execute ('SELECT ili.product_code as "Product Code", p.name as "Product Name" '
                    ' , SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.product_total) as "Total Value Sold" '
                    ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                    '   JOIN product p ON ili.product_code = p.code '
                    ' GROUP BY p.code, ili.product_code, p.name '
                    ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)

    return render(request, 'report_products_sold.html', dataReport)

def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result