__author__ = 'dfitzgerald'
from django.shortcuts import render

def index(request):
    return render(request, 'swiftseqgui2/www/home.html')
