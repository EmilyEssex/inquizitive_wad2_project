from django.shortcuts import render
from django.gttp import HttpResponse


# Create your views here.

def index(request):
    return HttpResponse("Homepage.")
