import boto3

class Database:
    client = boto3.client('dynamodb',aws_access_key_id='AKIAWLU3NUWTG74PCASA', aws_secret_access_key='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', region_name='us-west-1')

    ''' Account Operations '''

    def get_account(self, accountNumber):
        response = self.client.get_item(
            TableName="Account",
            Key={
                'accountNumber': str(accountNumber)
            },            
        )
        return response 

    def create_account(self, recordID, accountNumber, balance, isClosed=False):
        accountStatus = "CLOSED" if isClosed else "OPEN"

        response = self.client.put_item(
            TableName="Account",
            Item={
                'accountNumber': {
                    'S': str(accountNumber)
                },
                'balance': {
                    'N': str(balance)
                },
                'accountStatus':{
                    'S': str(accountStatus)
                }
            }
        )

        return True
    

    def update_account(self, accountNumber, balance = None, accountStatus = None):
        item = dict()
        if balance:
            response = self.client.update_item(
                TableName="Account",
                Key={
                    'accountNumber' : {
                        'S' : accountNumber
                    },
                },
                UpdateExpression="set balance = :r",
                ExpressionAttributeValues={
                    ':r': {
                        'N': balance
                    }
                }
            )
        if accountStatus:
            response = self.client.update_item(
                TableName="Account",
                Key={
                    'accountNumber' : {
                        'S' : accountNumber
                    },
                },
                UpdateExpression="set accountStatus = :r",
                ExpressionAttributeValues={
                    ':r': {
                        'S': accountStatus
                    }
                }
            )
        print(item)
            
        return True

    ''' Customer Operations '''

    def create_customer(self, accountNumber, firstName, lastName):
        response = self.client.put_item(
            TableName="Customer",
            Item={
                'accountNumber': {
                    'S': str(accountNumber)
                },
                'firstName': {
                    'S': str(firstName)
                },
                'lastName': {
                    'S': lastName
                }
            }
        )
        return True
        
    ''' Transaction Operations '''

    def create_transaction(self, amount, transaction_type, associatedAccount):
       response = self.client.put_item(
            TableName="Transaction",
            Item={
                'amount': {
                    'N': str(amount)
                },
                'transaction_type': {
                    'S': str(transaction_type)
                },
                'accountNumber': {
                    'S': associatedAccount
                }
            }
        )


Database().create_account(2, str(4), "4.00")
Database().update_account("4", balance="14.00")
Database().create_transaction("18.00", "Debit", "2")
print(Database().get_account("2"))
#Database().update_account("4", accountStatus="CLOSED")