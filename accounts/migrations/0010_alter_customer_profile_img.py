# Generated by Django 5.0.4 on 2024-04-07 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_customer_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_img',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
    ]
