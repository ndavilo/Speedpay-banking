from django.db import models
# to create a token each time a user is created
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from random import randint
import secrets
from django.contrib.auth.hashers import make_password


class Customer(models.Model):
    """
        A model representing a customer.

        Fields:
        first_name (CharField): First name of the customer.
        middle_name (CharField): Middle name of the customer, can be blank.
        last_name (CharField): Last name of the customer.
        phone_number (CharField): Phone number of the customer, unique.
        email (EmailField): Email of the customer, unique.
        address (CharField): Address of the customer.
        photo (ImageField): Profile photo of the customer, can be blank.
        deleted (BooleanField): Indicates if the customer has been deleted.

        Methods:
        str: Returns the email of the customer as a string representation.
    """
    
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.email

# one customer can have more than one account numbers


class Account(models.Model):
    """
    This model represents a bank account belonging to a customer.

    Attributes:
        customer (ForeignKey): The customer who owns the account.
        account_type (CharField): The type of the account.
        amount (FloatField): The current balance of the account.
        date (DateTimeField): The date and time the account was created.
        tansaction_key (IntegerField): A unique identifier for each transaction.
        id (IntegerField): A unique identifier for the account, automatically generated upon creation.
        flag (BooleanField): A flag for account status.
        closed (BooleanField): Indicates whether the account has been closed or not.

    Methods:
        save(self, *args, **kwargs): Override the save method to automatically generate a unique id for the account.
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
        Override the save method to automatically generate a unique id for the account.

        Args:
            *args: Any additional arguments to pass to the superclass.
            **kwargs: Any additional keyword arguments to pass to the superclass.

        Returns:
            None

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
    Model for Withdraw transactions. 
    
    This class represents a withdraw transaction in the system. It contains information about the amount of the
    withdraw, the date and time of the transaction, and the related account. 
    
    Attributes:
        amount (float): The amount of the withdraw.
        date (datetime): The date and time of the transaction.
        account (ForeignKey): The account associated with this withdraw transaction.
        id (CharField): A unique identifier for the transaction.
    
    """
    amount = models.FloatField()
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    account = models.ForeignKey(
        Account, related_name='withdraw_account', on_delete=models.CASCADE)
    id = models.CharField(primary_key=True, editable=False, max_length=32)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to assign a unique id to the transaction if it's a new one.
        
        The method generates a unique identifier for the transaction using the `secrets` library and assigns it 
        to the `id` field. It then calls the parent class's `save` method to persist the changes.
        """
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
    Model for Deposit transactions.
    
    Attributes:
        amount (float): The amount of the deposit.
        date (datetime): The date and time of the transaction.
        account (ForeignKey): The account associated with this deposit transaction.
        id (CharField): A unique identifier for the transaction.
    """
    amount = models.FloatField()
    date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    account = models.ForeignKey(
        Account, related_name='deposit_account', on_delete=models.CASCADE,
        verbose_name='Account', help_text='The account associated with this deposit transaction.')
    id = models.CharField(primary_key=True, editable=False, max_length=32)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to assign a unique id to the transaction if it's a new one.
        
        The method generates a unique identifier for the transaction using the `secrets` library and assigns it 
        to the `id` field. It then calls the parent class's `save` method to persist the changes.
        """
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
    Model for Transfer transactions.
    
    Attributes:
        debit (ForeignKey): The account the transfer will be debited from.
        credit (ForeignKey): The account the transfer will be credited to.
        amount (float): The amount of the transfer.
        date (datetime): The date and time of the transaction.
        id (CharField): A unique identifier for the transaction.
    """
    debit = models.ForeignKey(
        Account, 
        related_name='debit_account', 
        on_delete=models.CASCADE,
        verbose_name='Debit Account', help_text='The account the transfer will be debited from.')
    credit = models.ForeignKey(
        Account, 
        related_name='credit_account', 
        on_delete=models.CASCADE,
        verbose_name='Credit Account', help_text='The account the transfer will be credited to.')
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
        """
        Overrides the default save method to assign a unique id to the transaction if it's a new one.
        
        The method generates a unique identifier for the transaction using the `secrets` library and assigns it 
        to the `id` field. It then calls the parent class's `save` method to persist the changes.
        """
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
    A model that represents an App User with One to One relation to `Account` model.
    
    Attributes:
        account (models.OneToOneField): A One to One relationship field with `Account` model.
        password (models.CharField): A character field that stores password of the user.
        varified (models.BooleanField): A boolean field that indicates whether the user is verified or not.
        
    """
    account = models.OneToOneField(
        Account, 
        related_name='app_account', 
        on_delete=models.CASCADE, 
        unique=True
        ) 
    password = models.CharField(max_length=100)
    varified = models.BooleanField(default=False)

 
    
class AppOTP(models.Model):
    """
    A Django model representing OTP generated for a user for a secure session.
    Model representing an OTP for a user account

    Attributes:
        id (int): Unique identifier for the OTP
        dateTime (datetime): Timestamp when the OTP was created
        closed (bool): Indicates if the OTP has been closed or not
        account (ForeignKey): Account associated with the OTP
    """
    id = models.IntegerField(primary_key=True, editable=False)
    dateTime = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    account = models.ForeignKey(Account, related_name='otp_account', on_delete=models.CASCADE) 

    def save(self, *args, **kwargs):
        """
        Save the instance to the database and generate a unique ID if it's a new instance.
        Override the default save method to generate a unique identifier for the OTP if not provided.
        Args:
            *args: Additional arguments
            **kwargs: Keyword arguments

        Returns:
            None
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
    """
    This model represents a token that is associated with an App User.

    Fields:
        id (CharField): Primary key and unique identifier for each token. Editable and max length is 32.
        dateTime (DateTimeField): The date and time the token was created.
        account (OneToOneField): One-to-one relationship with the `Account` model.

    """
    id = models.CharField(
        primary_key=True, 
        editable=False, 
        max_length=32
        )
    dateTime = models.DateTimeField(
        auto_now_add=True
        )
    account = models.OneToOneField(
        Account, 
        related_name='token_account', 
        on_delete=models.CASCADE
        ) 

    def save(self, *args, **kwargs):
        """
        This is used to create unique token ID's by using the `secrets.token_hex(16)` function.

        """
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
    This function creates a new `Token` object associated with `instance` every time a new `settings.AUTH_USER_MODEL` object is saved.

    Args:
        sender (class): The class that triggered the signal.
        instance (object): The object that was saved.
        created (bool): Whether the instance was created or updated.
        **kwargs: Additional keyword arguments.
    """
    if created:
        Token.objects.create(user=instance)



class POS_Customer(models.Model):
    """
    This model represents a customer in the system.

    Attributes:
        fullName (CharField): The full name of the customer.
        phoneNumber (CharField): The phone number of the customer.
        email (EmailField): The email of the customer.
        workAddress (CharField): The work address of the customer.
        accountNumber (ForeignKey): The account number of the customer, linked to the Account model.
        bankName (CharField): The bank name of the customer.
        nin (CharField): The NIN of the customer.
        bvn (CharField): The BVN of the customer.
        refereeFullName (CharField): The full name of the referee.
        refereeAddress (CharField): The address of the referee.
        refereeNIN (CharField): The NIN of the referee.
        refereeBVN (CharField): The BVN of the referee.
        refereeAccountNumber (CharField): The account number of the referee.
        refereeBankName (CharField): The bank name of the referee.
        profilePicture (ImageField): The profile picture of the customer.

    """
    fullName = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    workAddress = models.CharField(max_length=255)
    accountNumber = models.ForeignKey(
        Account, related_name='pos_account', on_delete=models.CASCADE)
    bankName = models.CharField(max_length=255)
    nin = models.CharField(max_length=255)
    bvn = models.CharField(max_length=255)
    refereeFullName = models.CharField(max_length=255)
    refereeAddress = models.CharField(max_length=255)
    refereeNIN = models.CharField(max_length=255)
    refereeBVN = models.CharField(max_length=255)
    refereeAccountNumber = models.CharField(max_length=255)
    refereeBankName = models.CharField(max_length=255)
    profilePicture = models.ImageField(upload_to='pos_profile_pictures/', null=True, blank=True)
    password = models.CharField(max_length=100)
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

