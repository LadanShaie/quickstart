from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'



class Category(db.Model):

    __tablename__ = 'categories'
     
    category_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    title = db.Column(db.String) #Value is an array, big issue, use to display category info to user 
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  

    user = db.relationship('User', backref='categories')

    def __repr__(self):
        return f'<Category category_id={self.category_id} category_title={self.title}>'


class Merchant(db.Model):

    __tablename__ = 'merchants'
     
    merchant_name = db.Column(db.String, nullable=False, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  

    user = db.relationship('User', backref='merchants')

    def __repr__(self):
        return f'<Merchant merchant_name={self.merchant_name}>'

class Budget(db.Model):

    __tablename__ = 'budgets'
     
    budget_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    status = db.Column(db.String)
    merchant_name = db.Column(db.String, db.ForeignKey('merchants.merchant_name'))
    spend_limit = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  

    user = db.relationship('User', backref='budgets')
    merchant = db.relationship('Merchant', backref='budgets')

    def __repr__(self):
        return f'<Budget budget_id={self.budget_id} spend_limit={self.spend_limit}>'


class Account(db.Model):

    __tablename__ = 'accounts'
     
    account_id = db.Column(db.String, primary_key=True)
    available_balance = db.Column(db.Float) #nested dict need value for [available]
    type = db.Column(db.String)
    name=db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship('User', backref='accounts')

    def __repr__(self):
        return f'<Account account_id={self.account_id} balance={self.available_balance}>' #balances not finished 


class Transaction (db.Model):

    __tablename__ = 'transactions'
     
    transaction_id = db.Column(db.Integer, autoincrement=True, primary_key=True) #autoincrement for now, once data is from bank remove autoincrement/make db.string and add transaction_id to seed_database.
    amount = db.Column(db.Float)  #amount needs to be float not int
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id')) # Use to group by and determine budget 
    date = db.Column(db.DateTime)
    merchant_name = db.Column(db.String, db.ForeignKey('merchants.merchant_name'))
    account_id = db.Column(db.String, db.ForeignKey('accounts.account_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


    account = db.relationship('Account', backref='transactions')
    user = db.relationship('User', backref='transactions')
    category = db.relationship('Category', backref=db.backref('transactions', lazy='dynamic'))
    merchant = db.relationship('Merchant', backref=db.backref('transactions', lazy='dynamic'))

    def __repr__(self):
        return f'<Transaction merchant_name={self.merchant_name} amount={self.amount}>'

#need to make transaction_category table (many to many)


def connect_to_db(flask_app, db_uri='postgresql:///budgetapp', echo=False):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    connect_to_db(app)