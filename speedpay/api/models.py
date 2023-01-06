from django.db import models
#to create a token each time a user is created
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from random import randint

class Customer(models.Model):
    first_name      = models.CharField(max_length=100)
    middle_name     = models.CharField(max_length=100, null=True, blank=True)
    last_name       = models.CharField(max_length=100)
    phone_number    = models.CharField(max_length=15, unique=True)
    email           = models.EmailField(unique=True)
    address         = models.CharField(max_length=200)
    photo           = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.email

#one customer can have two account numbers
class Account(models.Model):
    customer        = models.ForeignKey(Customer, related_name='customer', null=True, on_delete=models.CASCADE)
    account_type    = models.CharField(max_length=10)
    amount          = models.FloatField()
    date            = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    tansaction_key  = models.IntegerField()
    id              = models.IntegerField(primary_key=True, editable=False)
    flag            = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = randint(20000000000, 30000000000)
                is_id_exist = Account.objects.filter(id=id).exists()
                
            self.id = id

        super().save(*args, **kwargs)

class Withdraw(models.Model):
    amount  =    models.FloatField()
    date    =      models.DateTimeField(blank=True, null=True, auto_now_add=True)
    account =   models.ForeignKey(Account, related_name='withdraw_account', on_delete=models.CASCADE)


class Deposit(models.Model):
    amount  =   models.FloatField()
    date    =   models.DateTimeField(blank=True, null=True, auto_now_add=True)
    account =   models.ForeignKey(Account, related_name='deposit_account', on_delete=models.CASCADE)


class Transfer(models.Model):
    debit   =   models.ForeignKey(Account, related_name='debit_account', on_delete=models.CASCADE)
    credit  =   models.ForeignKey(Account, related_name='credit_account', on_delete=models.CASCADE)
    amount  =   models.FloatField()
    date    =   models.DateTimeField(blank=True, null=True, auto_now_add=True)


#to create a token each time a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Withdraw) 
def create_product(sender, instance, created, **kwargs):
    amount = instance.amount
    id = instance.account.id
    account = Account.objects.get(id=id)
    account.amount = account.amount - amount
    account.save()

@receiver(post_save, sender=Deposit) 
def create_product(sender, instance, created, **kwargs):
    amount = instance.amount
    id = instance.account.id
    account = Account.objects.get(id=id)
    account.amount = account.amount + amount
    account.save()

@receiver(post_save, sender=Transfer) 
def create_product(sender, instance, created, **kwargs):
    amount = instance.amount
    debit_id = instance.debit.id
    credit_id = instance.credit.id
    credit_account = Account.objects.get(id=credit_id)
    credit_account.amount = credit_account.amount + amount
    credit_account.save()
    debit_account = Account.objects.get(id=debit_id)
    debit_account.amount = debit_account.amount - amount
    debit_account.save()