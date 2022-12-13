from django.db import models
#to create a token each time a user is created
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class Customer(models.Model):
    first_name      = models.CharField(max_length=100)
    middle_name     = models.CharField(max_length=100, null=True, blank=True)
    last_name       = models.CharField(max_length=100)
    phone_number    = models.CharField(max_length=15)
    email           = models.EmailField()
    address         = models.CharField(max_length=200)
    photo           = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.email

#one customer can have two account numbers
class Account(models.Model):
    customer =      models.ForeignKey(Customer, related_name='customer', null=True, on_delete=models.CASCADE)
    account_number =models.CharField(max_length=12)
    account_type =  models.CharField(max_length=10)
    amount =        models.FloatField()
    date =      models.DateTimeField(blank=True, null=True, auto_now_add=True)
    tansaction_key =models.IntegerField()

class Withdraw(models.Model):
    amount =    models.FloatField()
    date =      models.DateTimeField(blank=True, null=True, auto_now_add=True)
    account =   models.ForeignKey(Account, related_name='withdraw_account', on_delete=models.CASCADE)

class Deposit(models.Model):
    amount =    models.FloatField()
    date =      models.DateTimeField(blank=True, null=True, auto_now_add=True)
    account =   models.ForeignKey(Account, related_name='deposit_account', on_delete=models.CASCADE)


#to create a token each time a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)