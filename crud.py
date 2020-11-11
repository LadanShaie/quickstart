"""CRUD operations."""

from model import db, User, Category, Merchant, Account, Budget, Transaction, connect_to_db
from datetime import datetime



def create_user(user_name, email, password):
    """Create and return a new user."""

    user = User(user_name=user_name,
                email=email, 
                password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_category(category_id, title):
    """Create and return a new category."""
    category = Category.query.filter_by(category_id=category_id).first()
                    
    #check if it exists in database to avoid repeating PK, if not add it
    if not category:
        category = Category(category_id=category_id, title=title)

    db.session.add(category)
    db.session.commit()

    return category


def create_merchant_name(merchant_name):
    """Create and return a new merchant name."""
    name = Merchant.query.filter_by(merchant_name=merchant_name).first()
                    
    #check if it exists in database to avoid repeating PK, if not add it
    if not name:
        name = Merchant(merchant_name=merchant_name)

    db.session.add(name)
    db.session.commit()

    return name



def create_budget(status, spend_limit, start_date, end_date, user, category_id, merchant_name):
    """Create and return a new budget."""

    budget = Budget(status=status,
                    spend_limit=spend_limit, 
                    start_date=start_date, 
                    end_date=end_date, 
                    user=user, 
                    category_id=category_id,
                    merchant_name=merchant_name)

    db.session.add(budget)
    db.session.commit()

    return budget

def create_account(account_id, available_balance, type, name, user):
    """Create and return a new account."""

    account = Account(account_id=account_id,
                      available_balance=available_balance, 
                      type=type,
                      name=name,
                      user=user)

    db.session.add(account)
    db.session.commit()

    return account

def create_transaction(transaction_id, amount, date, merchant_name, user, account_id, category_id):
    """Create and return a new transaction."""

    transaction = Transaction(transaction_id=transaction_id,
                                amount=amount,
                                date=date,
                                merchant_name=merchant_name,  
                                user=user, 
                                account_id=account_id,
                                category_id=category_id)

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

# def get_amount_by_merchant():
#     Transaction.query.with_entities(func.sum(Transaction.amount)).filter(Transaction.amount > 0).order_by(Transaction.name).all()
#     print (Transaction.name)

# SQL version: SELECT name, SUM(amount) FROM transactions GROUP BY name;

def get_transactions():
    """Return all transactions."""

    return Transaction.query.all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)