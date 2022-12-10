from django.contrib import admin
from .models import *

#set admin site header
admin.site.site_header = 'Flight Management'

# Register your models here.
admin.site.register(Flight)
admin.site.register(Ticket)
admin.site.register(Customer)
admin.site.register(Flightclass)