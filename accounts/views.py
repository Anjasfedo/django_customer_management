from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Order, Customer, Product
from .forms import OrderForm

# Create your views here.


def dashboard(request):
    """
    Render dashboard page
    """
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
    """
    Render products page
    """
    context = {
        'products': Product.objects.all()
    }

    return render(request, 'accounts/products.html', context)


def customers(request, pk):
    """
    Render customer page with primary key as parameter
    """
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_order
    }

    return render(request, 'accounts/customers.html', context)


def create_order(request, pk):
    """
    Render create order of inlin formset with primary key of customer as parameter
    """
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
        # * Form without inline set
        # form = OrderForm(request.POST)

        forms = OrderFormSet(request.POST, instance=customer)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard')

    # * Form without inline set
    # form = OrderForm(initial={'customer': customer})

    forms = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    context = {
        'forms': forms
    }

    return render(request, 'accounts/order_form.html', context)


def update_order(request, pk):
    """
    Render form page for update with primary key of order as parameter
    """
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
    """
    Render order_delete with primary key of order as parameter
    """
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')

    context = {
        'order': order
    }

    return render(request, 'accounts/order_delete.html', context)
