from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # return HttpResponse("Hello world! You are in the bikes app!")
    return render(request, 'templates/bikes/bikes.html', {})