import base64
import os
import datetime
import plaid
import json
import time
from model import connect_to_db
import crud
from flask import (Flask, render_template, request, flash, session,
                   redirect)
# from flask_session import Session

from jinja2 import StrictUndefined


# app.config['SECRET_KEY']= "devhhjdjciijkdjjkkkdkkhebbfhhfuksne" 
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_PERMANENT']= False 
# Session(app)



app = Flask(__name__)
app.secret_key = "devhhjdjciijkdjjkkkdkkhebbfhhfuksne"
app.jinja_env.undefined = StrictUndefined

@app.route('/', methods=['GET'])
def show_homepage(): 
    """View homepage."""

    return render_template('homepage.html')


@app.route('/', methods=['POST'])
def from_homepage(): 
    """Redirect to create_account or login page from homepage."""

    login_choice = request.form.get('login')
    create_account_choice = request.form.get('create_account')

    if create_account_choice == 'Create an account':
        return redirect('/create_account')
    elif login_choice == 'Login':
        return redirect('/login')



@app.route('/create_account')
def create_account():
    """View create account page."""
    return render_template('create_account.html')

@app.route('/create_accout', methods=['POST'])
def create_account_info():
    """Create a new account + Store user info in db"""
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
    else:
        added_user = crud.create_user(user_name, email, password)
        session['user_id'] = added_user.user_id
        flash('Account created! Please log in.')

    return redirect('/login')


@app.route('/login', methods=['GET'])
def login():
    """View login page."""

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_info():
    """Allow user to login by verfication + Store login info in db""" 

    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)
    if user:  
        if password == user.password: 
            session['user_id'] = user.user_id
            return redirect('/overview')
    
    flash('Incorrect email or password. Please try again.')
    return redirect('/login')



@app.route('/overview', methods=['GET'])
def overview_data():
    """View transactions and account balance information"""

    user = crud.get_user_by_user_id(session['user_id'])
    return render_template('overview.html', transactions = user.transactions, accounts = user.accounts)
    
    # #Movie ratings lab 
    # transactions = crud.get_transactions()
    # return render_template('overview.html', transactions=transactions)




if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")