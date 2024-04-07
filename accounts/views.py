# Import django packages
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Import models, forms, filters
from .models import Order, Customer, Product
from .forms import OrderForm, UserRegisterForm, UserLoginForm, CustomerForm
from .filters import OrderFilter
from .decorators import already_login, allow_users, admin_only

# Create your views here.


@already_login
def user_register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')

            user.groups.add(group)

            Customer.objects.create(user=user)

            messages.success(request, f'User {username} created')
            return redirect('dashboard')

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)


@already_login
def user_login(request):
    form = UserLoginForm()

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            form.clean()
            user = form.get_user()
            login(request, user)
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
@allow_users(allow_roles=['customer'])
def user_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer) 
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance= customer)
        if form.is_valid():
            form.save()
            return redirect('user_settings')
    
    context = {
        'form': form
    }

    return render(request, 'accounts/settings.html', context)


@admin_only
@allow_users(allow_roles=['admin'])
def dashboard(request):
    """
    Render dashboard page
    """
    orders = Order.objects.all()
    context = {
        'orders': orders.order_by("-id")[:5],
        'customers': Customer.objects.all(),
        'total_orders': orders.count(),
        'delivered': orders.filter(status='Delivered').count(),
        'pending': orders.filter(status='Pending').count()
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required()
@allow_users(allow_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    context = {
        'orders': orders,
        'total_orders': orders.count(),
        'delivered': orders.filter(status='Delivered').count(),
        'pending': orders.filter(status='Pending').count()
    }

    return render(request, 'accounts/user_page.html', context)


@login_required()
@allow_users(allow_roles=['admin'])
def products(request):
    """
    Render products page
    """
    context = {
        'products': Product.objects.all()
    }

    return render(request, 'accounts/products.html', context)


@login_required()
@allow_users(allow_roles=['admin'])
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
@allow_users(allow_roles=['admin'])
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
@allow_users(allow_roles=['admin'])
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
@allow_users(allow_roles=['admin'])
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
