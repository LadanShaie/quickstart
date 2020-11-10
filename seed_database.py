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
user_name= 'Testy'
email = 'user1@test.com' 
password = 'test1'
user= crud.create_user(user_name, email, password)

# Load transaction data from JSON file
with open('data/transactions.json') as f:
    transaction_data = json.loads(f.read())

# Load account and balance data from JSON file
with open('data/balances.json') as f:
    balances_data = json.loads(f.read())
    

# Populate category table in budgetapp db
categories_in_db = []
for item in transaction_data['transactions']:
        category_id = (item['category_id'])
        title = (item['category']) #It stores as a dict not a list or str. 
      
        db_category = crud.create_category(category_id,
                            title)

        categories_in_db.append(db_category)

# Populate budget table in budgetapp db , LATER through user inputs. 

        
# Populate account table in budgetapp db
for item in balances_data['accounts']:
        account_id, type, name = (item['account_id'],
                            item['type'],
                            item['name'])

        available_balance = (item['balances']['available'])

        crud.create_account(account_id,
                            available_balance,
                            type,
                            name)


# Populate transaction table in budgetapp db + store transactions in list 
transactions_in_db = []
for item in transaction_data['transactions']:
        transaction_id, amount, name, account_id, category_id = (item['transaction_id'],
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
                                                account_id=account_id,
                                                category_id=category_id)

        transactions_in_db.append(db_transaction)

    #blocker: how to populate fk in transaction table when primary key wasn't autoincremented. What about category and acccount parameters? 
    # 
    # how to move transactions reponse to this file
    # api call keep in server.py after data added to db?
    # transactions_in_db = []
    # transactions_in_db.append(db_transaction)

    
