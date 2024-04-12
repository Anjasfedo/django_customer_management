from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('', views.dashboard, name='dashboard'),
    path('user/', views.user_page, name='user_page'),

    path('settings/', views.user_settings, name='user_settings'),

    path('products/', views.products, name='products'),

    path('customers/<int:pk>/', views.customers, name='customers'),

    path('create_order/<int:pk>/', views.create_order, name="create_order"),
    path('update_order/<int:pk>/', views.update_order, name="update_order"),
    path('delete_order/<int:pk>/', views.delete_order, name="delete_order"),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_complete'),

]
