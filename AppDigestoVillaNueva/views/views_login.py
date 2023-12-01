from django.shortcuts import  redirect, render
from django.views.generic import View

# Create your views here.

def index(request):
    return render(request, 'home.html')