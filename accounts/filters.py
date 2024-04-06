from django_filters import FilterSet, DateFilter, CharFilter
from django.forms import DateInput
from .models import Order
from datetime import datetime


class OrderFilter(FilterSet):
    start_date = DateFilter(field_name='created_at', lookup_expr='gte', widget=DateInput(
        attrs={'type': 'date'}), label='Start Date')
    end_date = DateFilter(field_name='created_at', lookup_expr='lte', widget=DateInput(
        attrs={'type': 'date'}), label='End Date')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'created_at']
