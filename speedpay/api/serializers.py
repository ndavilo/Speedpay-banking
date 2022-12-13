from .models import Customer, Account, Withdraw, Deposit 
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('__all__')

class CustomerSerializer(serializers.ModelSerializer):
    customer = AccountSerializer(many=True,)
    class Meta:
        model = Customer
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