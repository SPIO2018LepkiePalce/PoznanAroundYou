from django.shortcuts import render
from django.http import HttpResponse

def default(response):
    return HttpResponse("this is stops")

# Create your views here.
