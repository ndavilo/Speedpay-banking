from .models import Account, Withdraw, Deposit 
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('__all__')


class WithdrawSerializer(serializers.ModelSerializer):
    account = AccountSerializer(many=True)
    class Meta:
        model = Withdraw
        fields = ('__all__')


class DepositSerializer(serializers.ModelSerializer):
    account = AccountSerializer(many=True)
    class Meta:
        model = Deposit
        fields = ('__all__')