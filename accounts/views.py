from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.


def home(request):
    context = {
        'orders': Order.objects.all().order_by("-id")[:5],
        'customers': Customer.objects.all(),
        'total_customers': Customer.objects.count(),
        'total_orders': Order.objects.count(),
        'delivered': Order.objects.filter(status='Delivered').count(),
        'pending': Order.objects.filter(status='Pending').count()
    }
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'accounts/products.html', context)


def customers(request):
    return render(request, 'accounts/customers.html', context={})
