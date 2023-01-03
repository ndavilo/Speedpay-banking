# Speedpay-banking
A Fintech API for Withdraws, Deposit and Balance

This API code allows the frontend access to Customer Account, Withdraw, Deposit and Balance. It also allows new registrations and Token is assigned immidatelly 

Open speedpay file to access the API

You will be allowed to create user using http://127.0.0.1:8000/register
Automatically AUTH TOKEN will be generated which can be viewed with http://127.0.0.1:8000/api-token-auth
Other fuctions can be performed with the following endpoints
{
    "customer": "http://127.0.0.1:8000/customer/",
    "account": "http://127.0.0.1:8000/account/",
    "withdraw": "http://127.0.0.1:8000/withdraw/",
    "deposit": "http://127.0.0.1:8000/deposit/"
}

documentation: https://chukwunonsos-organization.gitbook.io/untitled/

Yet to be implimented:
1. Account number should be unique
2. Account balancing after each withdrawal and deposit (which can be done on the frontend)
3. End of day / monthly account balancing 