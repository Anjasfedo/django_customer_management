from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('products', views.products, name='products'),
    path('customers/<int:pk>', views.customers, name='customers')
]
