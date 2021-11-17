from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

# import boto3

# dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

app = FastAPI()

class Account(BaseModel):
    ID: int
    accountNumber: int
    balance: float
    status: bool

class User(BaseModel):
    firstName: str
    lastName: str
    ID: int
    associatedAccount: Account
    
class Transaction(BaseModel):
    id: int
    amount: float #always postive through error if not
    transactionType: bool #true = Credit, false = Debit
    # associatedAccount: Account


tempAccountUserTable = {} #accountNumber: user
class AccountNumbers:
    def __init__(self):
        self.numbers = 1
    def get(self):
        toReturn = self.numbers
        self.numbers += 1
        return toReturn

accountNumbers = AccountNumbers()

    

@app.get("/")
def read_root():
    return "test"


@app.get("/api/CustomerAccount/GetCustomerAccountByAccountNumber/{accountNumber}")
def retrieveCustomerAccount(accountNumber:int):
    user = tempAccountUserTable[accountNumber]
    return user


@app.post("/api/CustomerAccount/OpenCustomerAccount/", response_model = User)
def openCustomerAccount(firstname: str, lastname: str):
    account = Account(ID=1, accountNumber=accountNumbers.get(), balance=0.0, status= True)
    user = User(firstName = firstname, lastName = lastname, ID = 1, associatedAccount = account)
    tempAccountUserTable[account.accountNumber] = user
    return user


@app.post("/api/CustomerAccount/CloseCustomerAccount/", response_model=User)
def closeCustomerAccount(accountNumber: int):
    user = tempAccountUserTable[accountNumber]
    user.associatedAccount.status = False
    return user


@app.post("/api/CustomerAccount/ApplyTransactionToCustomerAccountAsync", response_model = User)
def applyTranscation(accountNumber : int, amount: float, transactionType: bool):
    user = tempAccountUserTable[accountNumber]
    user.associatedAccount.balance += amount if transactionType else -amount
    return user