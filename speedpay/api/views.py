from .models import AppUserToken, Customer, Account, Withdraw, Deposit, Transfer, AppUser, AppOTP
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
from .models import POS_Customer
from .serializers import POSCustomerSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_jwt.settings import api_settings


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

        Required Fields:

            customer (ForeignKey): The customer who owns the account.
            account_type (CharField): The type of the account.
            amount (FloatField): The current balance of the account.
            tansaction_key (IntegerField): A unique identifier for each transaction.
            id (IntegerField): A unique identifier for the account, automatically generated upon creation.
            flag (BooleanField, default is False): A flag for account status.
            closed (BooleanField, default is False): Indicates whether the account has been closed or not.

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
    Only authenticated users are allowed.

    API endpoint that allows to:
        * List all withdraws,
        * Create a new withdraw,
        * Retrieve details of a withdraw.

    Required Fields:
    amount (float): The amount of the withdraw.
    account (ForeignKey): The account associated with this withdraw transaction.

    Documentation: endpoint/docs/

    Filter the list of withdraws by `amount` and search for withdraw by `amount`.
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

        Required Fields:
        amount (float): The amount of the deposit.
        account (ForeignKey): The account associated with this deposit transaction.

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

        Required Fields:
        debit (ForeignKey): The account the transfer will be debited from.
        credit (ForeignKey): The account the transfer will be credited to.
        amount (float): The amount of the transfer.

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
    Verify user credentials and return token and username if verified.

    Args:
        request (dict):
            username (str): User's username.
            password (str): User's password.

    Returns:
        JSON response:
            {'detail': 'Please provide both username and password'}: If either `username` or `password` is missing.
            {'detail': 'UserName Invalid Credentials'}: If the provided `username` is not found.
            {'detail': 'Password Invalid Credentials'}: If the provided `password` is incorrect.
            {'token': token.key, 'user': username}: If the user's credentials are valid.
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


# APP USERS

class CreateAppUserView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
        All users with account number are allowed to register.
        after registration an OTP will be sent to your account's email for final verification

        Required Fields:


        Documentation: 'endpoint/docs/'

    """
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer


@api_view(["POST"])
def app_Authentication(request):
    """
    Verify user credentials and return account and customer information if verified.

    Args:
        request (dict):
            account (str): ID of the user's account.
            token (str): User's token.

    Returns:
        JSON response:
            {'detail': 'Please provide account and token'}: If either `account` or `token` is missing.
            {'detail': 'Invalid token'}: If the provided `token` is not found.
            {'detail': 'User already verified'}: If the account has already been verified.
            {'detail': 'App token verified'}: If the user's credentials are valid and the token is verified.
    """
    input_account = request.data.get("account")
    token = request.data.get("token")
    if token is None:
        return Response({'detail': 'Please provide token'})
    else:
        try:
            token_acc = AppOTP.objects.get(id=token)

        except AppOTP.DoesNotExist:
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


@api_view(['POST'])
def app_user_login_authentication(request):
    """
    Authenticate an app user and return relevant details.

    Args:
        request (HttpRequest): The request object. It should contain the following data:
            - account: ID of the account to be authenticated
            - password: password of the app user

    Returns:
        Response object:
            - If account or password is missing: {'detail': 'Please provide both account and password'}
            - If account is invalid: {'detail': 'Invalid Account'}, status=404
            - If account is not verified: {'detail': 'Verify this account or visit bank'}, status=401
            - If app user doesn't exist: {'detail': 'Invalid App User, Please Register'}, status=404
            - If password is incorrect: {'detail': 'Invalid Password'}, status=401
            - If successful: {'token': app_token.id, 'account': account, 'customer': serializer.data}, status=200
    """
    # code for authentication
    input_account = request.data.get("account")
    input_password = request.data.get("password")

    if input_account is None or input_password is None:
        return Response({'detail': 'Please provide both account and password'})

    try:
        account = Account.objects.get(id=input_account).id
    except Account.DoesNotExist:
        return Response({'detail': 'Invalid Account'}, status=status.HTTP_404_NOT_FOUND)

    try:
        app_account = AppUser.objects.get(account=account)

        if app_account.varified is False:
            return Response({'detail': 'Verify this account or visit bank'}, status=status.HTTP_401_UNAUTHORIZED)

        if app_account.password != input_password:
            return Response({'detail': 'Invalid Password'}, status=status.HTTP_401_UNAUTHORIZED)

    except AppUser.DoesNotExist:
        return Response({'detail': 'Invalid App User, Please Register'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        app_token = AppUserToken.objects.get(account=account)
        account_array = Account.objects.get(id=account)
        customer_id = account_array.customer
        customer = Customer.objects.get(email=customer_id)
        serializer = CustomerSerializer(customer)
        return Response({'token': app_token.id, 'account': account, 'customer': serializer.data},
                        status=status.HTTP_200_OK)


def isAuthorizedUser(input_token):
    """
        Check if the provided token is a valid token for an authorized app user

        Args:
        input_token (str): Token to be verified

        Returns:
        dict: A dictionary with two keys, 'status' (bool) indicating if the token is valid, and 'message' (str)
        containing either the account object or error message.

        """
    try:
        token = AppUserToken.objects.get(id=input_token)
        account_id = token.account.id
        account = Account.objects.get(id=account_id)

        return {'status': True, 'message': account}

    except AppUserToken.DoesNotExist:
        return {'status': False, 'message': 'Invalid Token'}


@api_view(['GET'])
def app_Account_View(request):
    """
    Retrieve customer's account information.
    Requires a valid app token in the request header. Returns all the customer's accounts and their details if the app token is verified. 

    - Request header:
        Authorization: <app_token>

    - Response:
        If successful, returns a JSON object with the customer's account information.
        If the app token is not provided, returns a JSON object with a detail message "Please provide token".
        If the app token is invalid, returns a JSON object with a detail message "Invalid Token".
        If the account is not verified, returns a JSON object with a detail message "Verify this account or visit bank".
        If the app user is not found, returns a JSON object with a detail message "Invalid App User, Please Register".

    - Documentation: 'endpoint/docs/'

    """
    input_token = request.headers.get('Authorization')

    if input_token is None:
        return Response({'detail': 'Please provide token'})

    auth = isAuthorizedUser(input_token=input_token)

    if auth['status'] is True:
        account_id = auth['message'].id
        account = Account.objects.get(id=account_id)
        customer_id = account.customer
        customer = Customer.objects.get(email=customer_id)

    else:
        return Response({'detail': 'Invalid Token'}, status=status.HTTP_404_NOT_FOUND)

    try:
        app_account = AppUser.objects.get(account=account_id)

        if app_account.varified is False:
            return Response({'detail': 'Verify this account or visit bank'}, status=status.HTTP_401_UNAUTHORIZED)

    except AppUser.DoesNotExist:
        return Response({'detail': 'Invalid App User, Please Register'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)


# POS
class POSCustomerCreateView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    POST API endpoint to create a POS customer.
    """
    queryset = POS_Customer.objects.all()
    serializer_class = POSCustomerSerializer


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

@api_view(['POST'])
def pos_customer_login(request):
    """
    API endpoint for POS customer login.
    The API verifies the account number and password provided by the customer and returns a JWT token along with the customer details and their accounts.

    Args:
        request (HttpRequest): The request object that contains the account number and password.

    Returns:
        JWT token (str): The JWT token assigned to the customer after successful verification.
        customer details (dict): The details of the customer, including the full name, phone number, email, work address, bank name, NIN, BVN, profile picture, etc.
        customer accounts (list): A list of the customer's accounts, including the account type, amount, transaction key, flag, and closed status.

    Raises:
        400 Bad Request: If the account number or password provided is incorrect.

    """
    account_number = request.data.get('account_number')
    password = request.data.get('password')
    customer = POS_Customer.objects.filter(accountNumber=account_number).first()
    if customer and check_password(password, customer.password):
        payload = jwt_payload_handler(customer)
        token = jwt_encode_handler(payload)
        customer_details = {
            'fullName': customer.fullName,
            'phoneNumber': customer.phoneNumber,
            'email': customer.email,
            'workAddress': customer.workAddress,
            'bankName': customer.bankName,
            'nin': customer.nin,
            'bvn': customer.bvn,
            'profilePicture': customer.profilePicture.url if customer.profilePicture else None
        }
        customer_accounts = [{
            'account_type': account.account_type,
            'amount': account.amount,
            'transaction_key': account.transaction_key,
            'flag': account.flag,
            'closed': account.closed
        } for account in customer.withdraw_account.all()]
        return Response({
            'token': token,
            'customer_details': customer_details,
            'customer_accounts': customer_accounts
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid account number or password'}, status=status.HTTP_400_BAD_REQUEST)
