from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from .models import Customer


@receiver(post_save, sender=User)
def customer_create(sender, instance, created, **kwargs):
    if created == True:
        group = Group.objects.get(name='customer')

        instance.groups.add(group)
        Customer.objects.create(user=instance, name=instance.username)

        print('Customer Created')


@receiver(post_save, sender=User)
def customer_update(sender, instance, created, **kwargs):
    if created == False:
        instance.customer.save()
        print('Customer updated')
