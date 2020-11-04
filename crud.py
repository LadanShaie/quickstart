from model import db, User, Category, Account, Budget, Transaction, connect_to_db
from datetime import datetime 


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, 
                password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_category(category_id, title):
    """Create and return a new category."""

    category = Category(category_id=category_id, 
                        title=title)

    db.session.add(category)
    db.session.commit()

    return category



def create_budget(spend_limit, start_date, end_date, user, category):
    """Create and return a new budget."""

    budget = Budget(spend_limit=spend_limit, 
                    start_date=start_date, 
                    end_date=end_date, 
                    user=user, 
                    category=category)

    db.session.add(budget)
    db.session.commit()

    return budget

def create_account(account_id, balances, type):
    """Create and return a new account."""

    account = Account(account_id=account_id,
                      balances=balances, 
                      type=type)

    db.session.add(account)
    db.session.commit()

    return account

def create_transaction(transaction_id, amount, date, name, account, budget, user, category):
    """Create and return a new transaction."""

    transaction = Transaction(transaction_id=transaction_id,
                                amount=amount, 
                                budget=budget, 
                                user=user, 
                                category=category)

    db.session.add(transaction)
    db.session.commit()

    return transaction

if __name__ == '__main__':
    from server import app
    connect_to_db(app)