from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerView, AccountView, WithdrawView, DepositView

router = DefaultRouter()
router.register('customer', CustomerView)
router.register('account', AccountView)
router.register('withdraw', WithdrawView)
router.register('deposit', DepositView)

urlpatterns = [
    path('', include(router.urls)),
]