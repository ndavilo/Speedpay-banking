from .models import Customer, Account, Withdraw, Deposit 
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('__all__')


class AccountSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=False)
    class Meta:
        model = Account
        fields = ('__all__')


class WithdrawSerializer(serializers.ModelSerializer):
    withdraw_account = AccountSerializer(many=True)
    class Meta:
        model = Withdraw
        fields = ('__all__')


class DepositSerializer(serializers.ModelSerializer):
    deposit_account = AccountSerializer(many=True)
    class Meta:
        model = Deposit
        fields = ('__all__')