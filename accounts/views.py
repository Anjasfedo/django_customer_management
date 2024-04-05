from django.shortcuts import render, redirect
from .models import Order, Customer, Product
from .forms import OrderForm

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


def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_order
    }

    return render(request, 'accounts/customers.html', context)


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    form = OrderForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/order_form.html', context)


def update_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    form = OrderForm(instance=order)

    context = {
        'form': form
    }

    return render(request, 'accounts/order_form.html', context)


def delete_order(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')

    context = {
        'order': order
    }

    return render(request, 'accounts/order_delete.html', context)
