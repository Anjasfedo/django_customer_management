from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('', views.dashboard, name='dashboard'),

    path('products', views.products, name='products'),

    path('customers/<int:pk>/', views.customers, name='customers'),

    path('create_order/<int:pk>/', views.create_order, name="create_order"),
    path('update_order/<int:pk>/', views.update_order, name="update_order"),
    path('delete_order/<int:pk>/', views.delete_order, name="delete_order")
]
