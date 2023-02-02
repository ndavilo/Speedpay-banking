from .models import AppOTP, AppUser, AppUserToken, Customer, Account, Withdraw, Deposit, Transfer
from .models import POS_Customer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

 # To validate transfer amount with the current balance


def validateAccount(id, amount):
    account = Account.objects.get(id=id)
    if float(account.amount) < float(amount):
        return True
    else:
        return False


def createTransfer(amount, debit_account_id, credit_account_id):

    credit_account = Account.objects.get(id=credit_account_id)
    credit_account.amount = credit_account.amount + amount
    credit_account.save()
    debit_account = Account.objects.get(id=debit_account_id)
    debit_account.amount = debit_account.amount - amount
    debit_account.save()


def createWithdraw(amount, id):

    account = Account.objects.get(id=id)
    account.amount = account.amount - amount
    account.save()


def createDeposit(amount, id):

    account = Account.objects.get(id=id)
    account.amount = account.amount + amount
    account.save()


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = ('__all__')

    def validate(self, attrs):
        id = attrs['account'].id
        amount = attrs['amount']
        if validateAccount(id, amount):
            raise serializers.ValidationError(
                {"insuficent balance"})

        if Account.objects.get(id=id).flag:
            raise serializers.ValidationError(
                {"Go to the bank"})

        createWithdraw(amount, id)
        return attrs


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('__all__')

    def validate(self, attrs):
        id = attrs['account'].id
        amount = attrs['amount']

        createDeposit(amount, id)
        return attrs


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('__all__')

    def validate(self, attrs):
        debit_account_id = attrs['debit'].id
        credit_account_id = attrs['credit'].id
        amount = attrs['amount']

        if debit_account_id == credit_account_id:
            raise serializers.ValidationError(
                {"You cant transfer to same account"})

        if validateAccount(debit_account_id, amount):
            raise serializers.ValidationError(
                {"insuficent balance"})

        if Account.objects.get(id=debit_account_id).flag:
            raise serializers.ValidationError(
                {"Go to the bank"})

        createTransfer(amount, debit_account_id, credit_account_id)

        return attrs


class AccountSerializer(serializers.ModelSerializer):
    withdraw_account = WithdrawSerializer(many=True, read_only=True)
    deposit_account = DepositSerializer(many=True, read_only=True)
    debit_account = TransferSerializer(many=True, read_only=True)
    credit_account = TransferSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ('__all__')


class CustomerSerializer(serializers.ModelSerializer):
    customer = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('__all__')
 
 
class AppOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppOTP
        fields = ('__all__')
        
        
class AppUserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUserToken
        fields = ('__all__')

               
class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('account','password')
        
    def validate(self, attrs):
        account_id = attrs['account']
        appOTP = AppOTP.objects.create(account = account_id)
        appOTP.save()
        appToken = AppUserToken.objects.create(account = account_id)
        appToken.save()
        
        return attrs


class POSCustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the POS_Customer model.
    """
    class Meta:
        model = POS_Customer
        fields = '__all__'