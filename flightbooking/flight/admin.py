from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = 'Flight Management'

admin.site.register(Flight)
admin.site.register(Ticket)
admin.site.register(Customer)