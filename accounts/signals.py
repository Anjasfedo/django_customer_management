from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer


@receiver(post_save, sender=User)
def customer_create(sender, instance, created, **kwargs):
    if created == True:
        Customer.objects.create(instance=User)
        print('Customer Created')


@receiver(post_save, sender=User)
def customer_update(sender, instance, created, **kwargs):
    if created == False:
        instance.customer.save()
        print('Customer updated')
