from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.products, name='home'),
    path('customers', views.customers, name='home')
]
