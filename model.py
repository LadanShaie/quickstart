from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'



class Category(db.Model):

    __tablename__ = 'categories'
     
    category_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String) #Value is an array, big issue, use to display category info to user 

    def __repr__(self):
        return f'<Category category_id={self.category_id} category_title={self.title}>'



class Budget(db.Model):

    __tablename__ = 'budgets'
     
    budget_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    spend_limit = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  

    user = db.relationship('User', backref='budgets')
    category = db.relationship('Category', backref='budgets')

    def __repr__(self):
        return f'<Budget budget_id={self.budget_id} spend_limit={self.spend_limit}>'


class Account(db.Model):

    __tablename__ = 'accounts'
     
    account_id = db.Column(db.Integer, primary_key=True)
    available_balance = db.Column(db.Float) #nested dict need value for [available]
    type = db.Column(db.String)

    def __repr__(self):
        return f'<Account account_id={self.account_id} balance={self.available_balance}>' #balances not finished 


class Transaction (db.Model):

    __tablename__ = 'transactions'
     
    transaction_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)  #amount needs to be float not int
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id')) # Use to group by and determine budget 
    date =  db.Column(db.DateTime)
    name = db.Column(db.String)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


    account = db.relationship('Account', backref='transactions')
    user = db.relationship('User', backref='transactions')
    category = db.relationship('Category', backref='transactions')


    def __repr__(self):
        return f'<Transaction name={self.name} amount={self.amount}>'




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