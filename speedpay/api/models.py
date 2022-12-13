from django.db import models


#to create a token each time a user is created
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class Account(models.Model):
    client =        models.CharField(max_length=12)
    account_type =  models.CharField(max_length=10)
    amount =        models.FloatField()
    tansaction_key =models.IntegerField(max_length=4)

class Withdraw(models.Model):
    amount =    models.FloatField()
    account =   models.ForeignKey(Account, related_name='account', on_delete=models.CASCADE)

class Deposit(models.Model):
    amount =    models.FloatField()
    account =   models.ForeignKey(Account, related_name='account', on_delete=models.CASCADE)


#to create a token each time a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)