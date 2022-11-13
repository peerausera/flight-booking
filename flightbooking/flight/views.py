
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import connection

from flight.models import *
import json

# Create your views here.
def index(request):
    data = {}
    return render(request, 'index.html', data)

def login(request):
    data = {}
    return render(request, 'login.html', data)
