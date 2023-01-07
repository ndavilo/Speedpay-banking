# Speedpay-banking
A Fintech API for Withdraws, Deposit and Balance

This API code allows the frontend access to Customer Account, Withdraw, Deposit and Balance. It also allows new registrations and Token is assigned immidatelly 

Open speedpay file to access the API

You will be allowed to create user using endpoint/register
Automatically AUTH TOKEN will be generated which can be viewed with endpoint/api-token-auth
Other fuctions can be performed with the following endpoints
{
    "customer": "endpoint/customer/",
    "account": "endpoint/account/",
    "withdraw": "endpoint/withdraw/",
    "deposit": "endpoint/deposit/",
    "register": "endpoint/register/",
    "transfer": "endpoint/transfer/"
}

documentation: 
endpoint/docs/
https://chukwunonsos-organization.gitbook.io/untitled/

Yet to be implimented:
1. Account number should be unique
2. Account balancing after each withdrawal and deposit (which can be done on the frontend)
3. End of day / monthly account balancing 