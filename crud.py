"""CRUD operations."""

from model import db, User, Category, Merchant, Account, Budget, Transaction, connect_to_db
from datetime import datetime
from decimal import Decimal as D



def create_user(user_name, email, password):
    """Create and return a new user."""

    user = User(user_name=user_name,
                email=email, 
                password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_category(category_id, title, user):
    """Create and return a new category."""
    category = Category.query.filter_by(category_id=category_id).first()
                    
    #check if it exists in database to avoid repeating PK, if not add it
    if not category:
        category = Category(category_id=category_id, title=title, user=user)

    db.session.add(category)
    db.session.commit()

    return category


def create_merchant_name(merchant_name, user):
    """Create and return a new merchant name."""
    name = Merchant.query.filter_by(merchant_name=merchant_name).first()
                    
    #check if it exists in database to avoid repeating PK, if not add it
    if not name:
        name = Merchant(merchant_name=merchant_name, user=user)

    db.session.add(name)
    db.session.commit()
    
    return name




def create_budget(status, spend_limit, start_date, end_date, user, merchant_name): # tried merchant_name got instance error
    """Create and return a new budget."""
    # budget = Budget.query.filter(merchant_name==merchant_name, end_date > datetime.now).first()
                    
    # #check if it exists in database to avoid repeating PK, if not add it
    # if not budget:
    #     print(status, spend_limit, start_date, end_date, user, merchant_name)

    budget = Budget(status=status,
                    spend_limit=spend_limit, 
                    start_date=start_date, 
                    end_date=end_date, 
                    user=user, 
                    merchant_name=merchant_name)

    print("created")

    db.session.add(budget)

    print("added")

    db.session.commit()

    return budget

def create_account(account_id, available_balance, type, name, user):
    """Create and return a new account."""
    account = Account.query.filter_by(account_id=account_id).first()
                    
    #check if it exists in database to avoid repeating PK, if not add it
    if not account:
        account = Account(account_id=account_id,
                        available_balance=available_balance, 
                        type=type,
                        name=name,
                        user=user)

        db.session.add(account)
        db.session.commit()

        return account

def create_transaction(amount, date, merchant_name, user, account_id):
    """Create and return a new transaction."""

    transaction = Transaction( amount=amount,
                                date=date,
                                merchant_name=merchant_name,  
                                user=user, 
                                account_id=account_id)

    db.session.add(transaction)
    db.session.commit()

    return transaction   

# CRUD functions for sessions and web app flow
def get_user_by_email(email):
    """Find a user by email"""

    return User.query.filter(User.email == email).first()


def get_user_by_user_id(user_id): 
    """Find user by user_id"""

    return User.query.get(user_id) 


# update account balance in db after new transaction is added 
def get_account_by_account_id (account_id, amount): 
    """Find account by account_id and subtract new transaction amount from available balance"""
    
    account = Account.query.get(account_id) 

    account.available_balance = (account.available_balance - int(amount))

    db.session.commit()
    
    return account 


def get_all_budgets():
    """Return all budgets."""

    return Budget.query.all()

def get_budgets():
    """Return all budgets."""

    return Budget.query.all()

def get_budget_by_budget_id(budget_id):
    """Return budget by budget_id."""

    return Budget.query.get(1)

# budget status function
def get_budget_status_by_budget_id(budget_id):
    
    budget = Budget.query.filter(Budget.budget_id == budget_id).first()
    transactions= Transaction.query.all()
    # print(transactions) #working 

    if budget.end_date > datetime.now():
       # print (budget.end_date) #working 

        sum_transactions = 0
        for transaction in transactions:
            #print (transaction.merchant_name) #working

            if (transaction.merchant_name == budget.merchant_name) and (transaction.date >= budget.start_date) and (transaction.date <= budget.end_date):
                sum_transactions += transaction.amount
        print (sum_transactions) #Issue: not getting sum of all transactions that fit criteria only getting one 
            
        if sum_transactions > budget.spend_limit: #messed up here, use pdb: helpful for many variables
            return  f'Uh oh! Your tree died! You went over budget and spent more than ${budget.spend_limit} at {budget.merchant_name}.'
        elif (sum_transactions < budget.spend_limit) or (sum_transactions == budget.spend_limit):
            return f"Your tree is still alive! You've been spending less than ${budget.spend_limit} at {budget.merchant_name}."
  
    # return f"Your tree is alive and well! You haven't spent a dime at {budget.merchant_name}." 

  

# def get_amount_by_merchant():
#     Transaction.query.with_entities(func.sum(Transaction.amount)).filter(Transaction.amount > 0).order_by(Transaction.name).all()
#     print (Transaction.name)
# SQL version: SELECT name, SUM(amount) FROM transactions GROUP BY name;


if __name__ == '__main__':
    from server import app
    connect_to_db(app)