"""CRUD operations."""

from model import db, User, Category, Merchant, Account, Budget, Transaction, connect_to_db
from datetime import datetime, date
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
  
    budget = Budget.query.filter(merchant_name==merchant_name, Budget.end_date >= datetime.now()).all()
    
    print (budget)  
    
    #check if it exists in database to avoid repeating PK, if not add it
    if not budget:

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

        return "budget-created"
    else: 
        return "budget-exsists"
    

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

    # Remember transactions are negative so we add below  
    account.available_balance = (account.available_balance + int(float(amount)))

    db.session.commit()
    
    return account 


# update account balance in db before selected transaction is deleted
def update_account_balance_post_trans_deleted (account_id, amount): 
    """Find account by account_id and add to-be-deleted transaction amount to available balance"""
    
    account = Account.query.get(account_id) 

    # Remember transactions are negative so the two negatives cancel each other and it becomes addition 
    account.available_balance = (account.available_balance - int(float(amount)))

    db.session.commit()
    
    return account 



########### Delete A Transaction ##############
def delete_transaction (transaction_id):
    """ Delete Transaction by transaction_id """
    
    transaction = Transaction.query.filter(Transaction.transaction_id == transaction_id).first()
    
    db.session.delete(transaction)
  
    db.session.commit()
    print ("Transaction Deleted") 
    
    return transaction_id


########### Delete A Budget ##############
def delete_budget (budget_id):
    """ Delete Budget by budget_id """
    
    budget = Budget.query.filter(Budget.budget_id == budget_id).first()
    
    
    db.session.delete(budget)
    
    db.session.commit()
    print ("Budget Deleted") 

    return budget_id
def get_all_budgets():
    """Return all budgets."""

    return Budget.query.all()

def get_budgets():
    """Return all budgets."""

    return Budget.query.all()

def get_budget_by_budget_id(budget_id):
    """Return budget by budget_id."""

    return Budget.query.get(1)

# Get budget status function
def get_budget_status_by_budget_id(budget_id):
    """Return budget status by budget_id."""
    budget = Budget.query.filter(Budget.budget_id == budget_id).first()
    transactions= Transaction.query.all()



    sum_transactions = 0
    for transaction in transactions:

        if (transaction.merchant_name == budget.merchant_name) and (transaction.date >= budget.start_date) and (transaction.date <= budget.end_date):
            sum_transactions += transaction.amount
            sum_transactions = abs(sum_transactions)
            #print (sum_transactions) #For testing  
        print(budget.end_date)
        
        
    if sum_transactions > budget.spend_limit:
        budget.status = "Tree is Dead"
        db.session.commit() #db session commit here after making budget.status = return statement
        return  f"Your tree died! You spent ${sum_transactions} instead of ${budget.spend_limit} at {budget.merchant_name}."
        
    elif (sum_transactions < budget.spend_limit) or (sum_transactions == budget.spend_limit):
        budget.status = "Tree is Alive"
        db.session.commit() #db session commit here after making budget.status = return statement
        return f"Your tree is alive! You've spent ${sum_transactions} of the allocated ${budget.spend_limit} budget for {budget.merchant_name}."



def get_garden_alive_count():
    """Return garden alive trees count."""

    budgets = Budget.query.all()

    count_alive = 0
    for budget in budgets:

        if (datetime.now() > budget.end_date) and (budget.status == "Tree is Alive"):
            count_alive += 1

    return count_alive 

def get_garden_dead_count():
    """Return garden dead trees count."""

    budgets = Budget.query.all()
    count_dead = 0

    for budget in budgets:

        if (datetime.now() > budget.end_date) and (budget.status == "Tree is Dead"):    
            count_dead += 1

    return count_dead 



if __name__ == '__main__':
    from server import app
    connect_to_db(app)