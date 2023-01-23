from .models import Customer, Account, Withdraw, Deposit, Transfer, AppUser, AppToken
from .serializers import AppUserSerializer, RegisterSerializer, CustomerSerializer, AccountSerializer, WithdrawSerializer, DepositSerializer, TransferSerializer
from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import action


# Class based view to register user
class RegisterUserAPIView(viewsets.ModelViewSet):
    """
    Only Admin users are allowed.

    Only perform the following:

        * List all the users,
        * Create new user,
        * Retrieve user,
        * Update user details,
        * Delete user

    Documentation: 'endpoint/docs/'

    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (IsAdminUser,)


class CustomerView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
        Only Authenticated users are allowed.

        Only perform the following:

            * List all the customers,
            * Create new customers,
            * Retrieve one customer,
            * Update customer details

        Documentation: 'endpoint/docs/'

    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id', 'phone_number', 'email', 'last_name']
    search_fields = ['id', 'phone_number', 'email', 'last_name']
    permission_classes = (IsAuthenticated,)


class AccountView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
        Only Authenticated users are allowed.

        Only perform the following:

            * List all the accounts,
            * Create new account,
            * Retrieve account,
            * Update account details

        Documentation: 'endpoint/docs/'

    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id']
    search_fields = ['id']
    permission_classes = (IsAuthenticated,)


class WithdrawView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    """
        Only Authenticated users are allowed.

        Only perform the following:

            * List all the withdrawals,
            * Create new withdrawal,
            * Retrieve withdrawal,

        Documentation: 'endpoint/docs/'

    """
    queryset = Withdraw.objects.all()
    serializer_class = WithdrawSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['amount']
    search_fields = ['amount']
    permission_classes = (IsAuthenticated,)


class DepositView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    """
        Only Authenticated users are allowed.

        Only perform the following:

            * List all the deposits,
            * Create new deposit,
            * Retrieve deposit,

        Documentation: 'endpoint/docs/'

    """
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['amount']
    search_fields = ['amount']
    permission_classes = (IsAuthenticated,)


class TransferView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    """
        Only Authenticated users are allowed.

        Only perform the following:

            * Create new transfer,
            * Retrieve transfer,

        Documentation: 'endpoint/docs/'

    """
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['amount', 'debit', 'credit']
    search_fields = ['amount', 'debit', 'credit']
    permission_classes = (IsAuthenticated,)


@api_view(["POST"])
def user_authentication(request):
    """
        All users are allowed.

        Only perform the following:

            * Check username,
            * Check password
            * Retrieve Token and User if both username and password is currect,

            when you catch the error, you can use: error.response.data.error 
            to get the error message. 

            common errors are: Invalid User and Ivalid Password

        Documentation: 'endpoint/docs/'

    """
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'detail': 'Please provide both username and password'})
    else:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'UserName Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)

        pwd_valid = authenticate(username=username, password=password)
        if pwd_valid:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,
                             'user': username}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Password Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)



#APP USERS

class CreateAppUserView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
        All users with account number are allowed to register.
        after registration an OTP will be sent to your account's email for final verification

        Documentation: 'endpoint/docs/'

    """
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
 
@api_view(["POST"])
def app_Authentication(request):
    """
        For verification of account,
        account= request.data.get("account")
        token = request.data.get("token")
        User is required to provide account and token sent to his email account or vist the bank
        Documentation: 'endpoint/docs/'

    """
    input_account= request.data.get("account")
    token = request.data.get("token")
    if token is None :
        return Response({'detail': 'Please provide token'})
    else:
        try:
            token_acc = AppToken.objects.get(id=token)
            print(token_acc)
            
        except AppToken.DoesNotExist:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            verify_account = AppUser.objects.get(account=input_account)
            
            if verify_account.varified is True:
                return Response({'detail': 'User already verified!'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            verify_account.varified = True
            verify_account.save()
            return Response({'detail': 'App token verified'}, status=status.HTTP_200_OK)
            
        except AppUser.DoesNotExist:
            return Response({'detail': 'Invalid account'}, status=status.HTTP_404_NOT_FOUND)
      

@api_view(['GET'])
def app_Account_View(request):
    """
        View User account,
        account= request.data.get("account")
        input_password = request.data.get("password")
        
        which when verified will return all the customer's accounts  and details 
    
        Documentation: 'endpoint/docs/'

    """
    account= request.data.get("account")
    input_password = request.data.get("password")
    
    if account is None or input_password is None:
        return Response({'detail': 'Please provide both account and password'})
    try: 
        account = Account.objects.get(id=account)
        customer_id = account.customer
        customer = Customer.objects.get(email=customer_id)
    except Account.DoesNotExist:
        return Response({'detail': 'Invalid Account'},status=status.HTTP_404_NOT_FOUND)
    
    try:          
        app_account = AppUser.objects.get(account=account)
        
        if app_account.varified is False:
            return Response({'detail': 'Verify this account or visit bank'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if app_account.password != input_password:
            return Response({'detail': 'Invalid Password'}, status=status.HTTP_401_UNAUTHORIZED)
        
    except AppUser.DoesNotExist:
        return Response({'detail': 'Invalid App User'},status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
        