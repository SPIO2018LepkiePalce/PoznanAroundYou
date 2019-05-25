from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .forms import DropdownForm

# Create your views here.
def index(request):
    #displays the default landing page
    form = DropdownForm()
    return render(request, 'landingpage/landingpage.html', {'form' : form})