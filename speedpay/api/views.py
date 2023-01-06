from .models import Customer, Account, Withdraw, Deposit
from .serializers import RegisterSerializer, CustomerSerializer, AccountSerializer, WithdrawSerializer, DepositSerializer
from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from urllib import request
from rest_framework.response import Response


def sample_view(request):
    current_user = request.user
    print (current_user.id)


#Class based view to register user
class RegisterUserAPIView(viewsets.GenericViewSet,mixins.CreateModelMixin,):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self,request):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class ViewUserAPIView(viewsets.GenericViewSet,mixins.CreateModelMixin,):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id', 'phone_number', 'email', 'last_name']
    search_fields = ['id', 'phone_number', 'email', 'last_name']
    permission_classes = (IsAuthenticated,)


class AccountView(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['account_number']
    search_fields = ['account_number']
    permission_classes = (IsAuthenticated,)


class WithdrawView(viewsets.ModelViewSet):
    queryset = Withdraw.objects.all()
    serializer_class = WithdrawSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['amount']
    search_fields = ['amount']
    permission_classes = (IsAuthenticated,)


class DepositView(viewsets.ModelViewSet):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['amount']
    search_fields = ['amount']
    permission_classes = (IsAuthenticated,)


    