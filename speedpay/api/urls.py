from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserAPIView, CustomerView, AccountView, WithdrawView, DepositView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('customer', CustomerView)
router.register('account', AccountView)
router.register('withdraw', WithdrawView)
router.register('deposit', DepositView)
router.register('register', RegisterUserAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name="api_token_auth")
]
