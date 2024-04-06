# Import django packages
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required

# Import models, forms, filters
from .models import Order, Customer, Product
from .forms import OrderForm, UserRegisterForm, UserLoginForm
from .filters import OrderFilter

# Create your views here.


def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'User {user} created')
            return redirect('dashboard')

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = UserLoginForm()

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            form.clean()
            user = form.get_user()
            login(request, user)
            print(user)
            messages.success(request, f'User {user} login')
            return redirect('dashboard')

    context = {
        'form': form
    }

    return render(request, 'accounts/login.html', context)


def user_logout(request):
    logout(request)

    return redirect('login')


@login_required()
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


@login_required()
def products(request):
    """
    Render products page
    """
    context = {
        'products': Product.objects.all()
    }

    return render(request, 'accounts/products.html', context)


@login_required()
def customers(request, pk):
    """
    Render customer page with primary key as parameter
    """
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()

    # * Search query
    customer_filter = OrderFilter(request.GET, queryset=orders)
    orders = customer_filter.qs

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_order,
        'customer_filter': customer_filter
    }

    return render(request, 'accounts/customers.html', context)


@login_required()
def create_order(request, pk):
    """
    Render create order of inlin formset with primary key of customer as parameter
    """
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)

    # * Form without inline set
    # form = OrderForm(initial={'customer': customer})
    forms = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        # * Form without inline set
        # form = OrderForm(request.POST)

        forms = OrderFormSet(request.POST, instance=customer)
        if forms.is_valid():
            forms.save()
            return redirect('dashboard')

    context = {
        'forms': forms
    }

    return render(request, 'accounts/order_form.html', context)


@login_required()
def update_order(request, pk):
    """
    Render form page for update with primary key of order as parameter
    """
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {
        'form': form
    }

    return render(request, 'accounts/order_form.html', context)


@login_required()
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
