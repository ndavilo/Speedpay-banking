from django.contrib import admin

from .models import Customer ,Account, Withdraw, Deposit, Transfer, AppUser, AppOTP, AppUserToken

# Register your models here.
admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Withdraw)
admin.site.register(Deposit)
admin.site.register(Transfer)
admin.site.register(AppUser)
admin.site.register(AppOTP)
admin.site.register(AppUserToken)