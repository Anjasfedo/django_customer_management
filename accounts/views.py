from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'accounts/dashboard.html', context={})

def products(request):
    return render(request, 'accounts/products.html', context={})

def customers(request):
    return render(request, 'accounts/customers.html', context={})
