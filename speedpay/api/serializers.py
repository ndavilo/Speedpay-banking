from .models import Customer, Account, Withdraw, Deposit, Transfer
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

 #To validate transfer amount with the current balance     
def validateAccount(id, amount):
  account = Account.objects.get(id=id)
  if float(account.amount) < float(amount):
    return True
  else:
    return False

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = ('__all__')
    
    def validate(self, attrs):
      id = attrs['account'].id
      if validateAccount(id, attrs['amount']):
        raise serializers.ValidationError(
            {"insuficent balance"})

      if Account.objects.get(id=id).flag:
          raise serializers.ValidationError(
              {"Go to the bank"})
      return attrs


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('__all__')
    

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('__all__')

    def validate(self, attrs):
        if attrs['debit'] == attrs['credit']:
            raise serializers.ValidationError(
              {"You cant transfer to same account"})

        id = attrs['debit'].id
        if validateAccount(id, attrs['amount']):
          raise serializers.ValidationError(
              {"insuficent balance"})

        if Account.objects.get(id=id).flag:
            raise serializers.ValidationError(
              {"Go to the bank"})

        return attrs

class AccountSerializer(serializers.ModelSerializer):
    withdraw_account = WithdrawSerializer(many=True, read_only = True)
    deposit_account = DepositSerializer(many=True, read_only = True)
    debit_account = TransferSerializer(many=True, read_only = True)
    credit_account = TransferSerializer(many=True, read_only = True)
    class Meta:
        model = Account
        fields = ('__all__')
        
class CustomerSerializer(serializers.ModelSerializer):
    customer = AccountSerializer(many=True, read_only = True)
    class Meta:
        model = Customer
        fields = ('__all__')