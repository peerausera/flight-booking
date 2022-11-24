"""flightbooking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from flight import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', views.login),
    path('login/signup/', views.CustomersSignup.as_view(), name='customersignup'),
    path('login/user/<username>', views.CustomerDetail.as_view(), name='loginuser'),
    path('flight/', views.Flightview),
    path('flight/createticket/', views.CreateTicket.as_view(), name='createticket'),
    path('ticket/', views.ticket),
    path('ticket/search/', views.SearchTicket.as_view(), name='searchticket'),
    path('ReportListAllTicket',views.ReportListAllTicket),
    path('ReportListAllCustomer',views.ReportListAllCustomer),
    path('FlightManagement', views.FMindex, name='FMindex'),
    # path('FlightManagement/list', views.InvoiceList.as_view(), name='invoice_list'),
    # path('FlightManagement/detail/<str:pk>/<str:pk2>', views.InvoiceDetail.as_view(), name='invoice_detail'),
    # path('FlightManagement/create', views.InvoiceCreate.as_view(), name='invoice_create'),
    # path('FlightManagement/update', views.InvoiceUpdate.as_view(), name='invoice_update'),
    # path('FlightManagement/delete', views.InvoiceDelete.as_view(), name='invoice_delete'),
    
]
