from django.db import models
# to create a token each time a user is created
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from random import randint
import secrets
#from django.contrib.auth.hashers import make_password


class Customer(models.Model):
    
    """
        This model is used to create customers on the database.
        first_name is a CharField with 100 as max
        middle_name is a CharField with 100 as max
        last_name is a CharField with 100 as max
        phone_number is a CharField with 15 as max with is unique
        email is email field with is unique 
        address is a CharField with 200 as max
        photo is an image field with can be left empty
        deleted is used to track deleted users which is set as false in default mode

    """
    
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200)
    photo = models.ImageField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.email

# one customer can have more than one account numbers


class Account(models.Model):
    
    """
        This model is used to create accounts on the database.
        customer = models.ForeignKey(
        Customer, related_name='customer', null=True, on_delete=models.CASCADE)
        account_type = models.CharField(max_length=10)
        amount = models.FloatField()
        date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
        tansaction_key = models.IntegerField()
        id = models.IntegerField(primary_key=True, editable=False)
        flag = models.BooleanField(default=False)
        closed = models.BooleanField(default=False)

    """
    customer = models.ForeignKey(
        Customer, related_name='customer', null=True, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10)
    amount = models.FloatField()
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    tansaction_key = models.IntegerField()
    id = models.IntegerField(primary_key=True, editable=False)
    flag = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        This is used to create unique account numbers from randint(20000000000, 30000000000)

        """
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = randint(20000000000, 30000000000)
                is_id_exist = Account.objects.filter(id=id).exists()

            self.id = id

        super().save(*args, **kwargs)


class Withdraw(models.Model):
    """
        This model is used to create withdraws on the database.
        amount = models.FloatField()
        date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
        account = models.ForeignKey(
            Account, related_name='withdraw_account', on_delete=models.CASCADE)
        id = models.CharField(primary_key=True, editable=False, max_length=32)

    """
    amount = models.FloatField()
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    account = models.ForeignKey(
        Account, related_name='withdraw_account', on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, editable=False, max_length=32)

    def save(self, *args, **kwargs):
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = secrets.token_hex(16)
                is_id_exist = Withdraw.objects.filter(id=id).exists()

            self.id = id

        super().save(*args, **kwargs)


class Deposit(models.Model):
    """
        This model is used to create deposits on the database.
        amount = models.FloatField()
        date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
        account = models.ForeignKey(
            Account, related_name='deposit_account', on_delete=models.CASCADE)
        id = models.CharField(primary_key=True, editable=False, max_length=32)

    """
    amount = models.FloatField()
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    account = models.ForeignKey(
        Account, related_name='deposit_account', on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, editable=False, max_length=32)

    def save(self, *args, **kwargs):
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = secrets.token_hex(16)
                is_id_exist = Deposit.objects.filter(id=id).exists()

            self.id = id

        super().save(*args, **kwargs)


class Transfer(models.Model):
    """
        This model is used to create transfers on the database.
        debit = models.ForeignKey(
            Account, 
            related_name='debit_account', 
            on_delete=models.CASCADE
            )
        credit = models.ForeignKey(
            Account, 
            related_name='credit_account', 
            on_delete=models.CASCADE
            )
        amount = models.FloatField()
        date = models.DateTimeField(
            blank=True, 
            null=True, 
            auto_now_add=True
            )
        id = models.CharField(
            primary_key=True, 
            editable=False, 
            max_length=32
            )

    """
    debit = models.ForeignKey(
        Account, 
        related_name='debit_account', 
        on_delete=models.CASCADE
        )
    credit = models.ForeignKey(
        Account, 
        related_name='credit_account', 
        on_delete=models.CASCADE
        )
    amount = models.FloatField()
    date = models.DateTimeField(
        blank=True, 
        null=True, 
        auto_now_add=True
        )
    id = models.CharField(
        primary_key=True, 
        editable=False, 
        max_length=32
        )

    def save(self, *args, **kwargs):
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = secrets.token_hex(16)
                is_id_exist = Transfer.objects.filter(id=id).exists()

            self.id = id

        super().save(*args, **kwargs)
            

class AppUser(models.Model):
    """
        This model is used to create app users on the database.
        account     = models.ForeignKey(Account, related_name='app_account', on_delete=models.CASCADE) 
        password    = models.CharField(max_length=100)
        varified    = models.BooleanField(default=False)

    """
    account     = models.OneToOneField(Account, related_name='app_account', on_delete=models.CASCADE, unique=True) 
    password    = models.CharField(max_length=100)
    varified    = models.BooleanField(default=False)

 
    
class AppOTP(models.Model):
    id          = models.IntegerField(primary_key=True, editable=False)
    dateTime    = models.DateTimeField(auto_now_add=True)
    closed      = models.BooleanField(default=False)
    account     = models.ForeignKey(Account, related_name='otp_account', on_delete=models.CASCADE) 

    def save(self, *args, **kwargs):
        """
        This is used to create unique account numbers from randint(100000, 1000000)

        """
        if not self.id:
            # if create new tree
            is_id_exist = True
            while is_id_exist:
                id = randint(100000, 1000000)
                is_id_exist = AppOTP.objects.filter(id=id).exists()

            self.id = id

        super().save(*args, **kwargs)
 
        
class AppUserToken(models.Model):
    id          = models.CharField(primary_key=True, editable=False, max_length=32)
    dateTime    = models.DateTimeField(auto_now_add=True)
    account     = models.OneToOneField(Account, related_name='token_account', on_delete=models.CASCADE) 

    def save(self, *args, **kwargs):
        if not self.id:
            is_id_exist = True
            while is_id_exist:
                id = secrets.token_hex(16)
                is_id_exist = AppUserToken.objects.filter(id=id).exists()

            self.id = id

        super().save(*args, **kwargs)
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def createAuthToken(sender, instance, created, **kwargs):
    """
        To create a token each time a user is created

    """
    if created:
        Token.objects.create(user=instance)



