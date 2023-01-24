from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserAPIView, CustomerView, AccountView, WithdrawView, DepositView, TransferView
from .views import user_authentication, CreateAppUserView, app_Authentication, app_Account_View, app_user_login_authentication
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register('customer', CustomerView)
router.register('account', AccountView)
router.register('withdraw', WithdrawView)
router.register('deposit', DepositView)
router.register('register', RegisterUserAPIView)
router.register('transfer', TransferView)
router.register('createAppUser', CreateAppUserView)


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name="api_token_auth"),
    path('docs/', include_docs_urls(title='Speedpay Banking')),
    path('auth/', user_authentication, name='auth'),
    path('app_auth/', app_Authentication, name='app_auth'),
    path('app_home/', app_Account_View, name='app_home'),
    path('app_user_auth/', app_user_login_authentication, name='app_user_auth'),
]
