"""Script to seed database."""
import os
import json
from datetime import datetime

import crud
import model
import server


os.system('dropdb budgetapp')
os.system('createdb budgetapp')
model.connect_to_db(server.app)
model.db.create_all()

# Adding one user
email = 'user@test.com' 
password = 'test'
user= crud.create_user(email, password)

# Load transaction data from JSON file
with open('data/transactions.json') as f:
    transaction_data = json.loads(f.read())

# Load account and balance data from JSON file
with open('data/balances.json') as f:
    balances_data = json.loads(f.read())
    

# Populate category table in budgetapp db
for item in transaction_data['transactions']:
        category_id, title = (item['category_id'],
                              item['category'])

        crud.create_category(category_id,
                            title)

# Populate account table in budgetapp db
for item in balances_data['accounts']:
        account_id, type = (item['account_id'],
                            item['type'])

        available_balance = (item['balances']['available'])

        crud.create_account(account_id,
                            available_balance,
                            type)


# Populate transaction table in budgetapp db + store transactions in list 

for item in transaction_data['transactions']:
        transaction_id, amount, name, account_id, = (item['transaction_id'],
                                        item['amount'],
                                        item['name'],
                                        item['account_id'],
                                        item['category_id'])

        date = datetime.strptime(item['date'], '%Y-%m-%d')

        db_transaction = crud.create_transaction(transaction_id=transaction_id,
                                                amount=amount,
                                                date=date,
                                                name=name,  
                                                user=user, 
                                                account=account,
                                                category=category)

                                                #question on category and acccount 

    # transactions_in_db = []
    # transactions_in_db.append(db_transaction)

    
