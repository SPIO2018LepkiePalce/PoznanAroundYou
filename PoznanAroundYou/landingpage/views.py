from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #displays the default landing page
    return render(request, 'templates/landingpage/index.html', {})