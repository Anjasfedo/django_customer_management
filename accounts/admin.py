from django.contrib import admin
from . import models

# Register your models here.
admin.site.register([models.Customer, models.Product, models.Order, models.Tag])