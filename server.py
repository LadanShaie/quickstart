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



app = Flask(__name__)
app.config['SECRET_KEY']= os.getenv('SECRET_KEY')
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
            return redirect('/budgets')
    
    flash('Incorrect email or password. Please try again.')
    return redirect('/login')






@app.route('/budgets', methods=['GET'])
def get_budgets():
    """View budgets page."""

    if session.get('user_id'):
        user = crud.get_user_by_user_id(session['user_id'])
        #flash('You made it!') #Test flash since not working, printing directly on screen, I want pop up 
        return render_template('budgets.html', budgets= user.budgets)
    else: 
        flash('Please login to proceed to this page.')
        return redirect('/login')  

@app.route('/budgets', methods=['POST'])
def redirect_to_create_budget():
    """Navigate from budgets page"""

    view_create_budget_page = request.form.get('create_budget_page')

    if view_create_budget_page == 'Create A New Budget':
        return redirect('/create_budget')     




@app.route('/create_budget', methods=['GET'])
def get_create_budget():
    """View create budget form."""

    if session.get('user_id'):
        user = crud.get_user_by_user_id(session['user_id'])
        return render_template('create_budget.html', transactions= user.transactions) #could user merchant table if you create user FK.
    else: 
        flash('Please login to proceed to this page.')
        return redirect('/login')  

@app.route('/create_budget', methods=['POST'])
def save_created_budget():
    """Create A Budget and send to db, user can view it after redirected back to budgets page."""    
    
    if session.get('user_id'):
        submit_budget_form = request.form.get("submit_budget_form")

        if  submit_budget_form  == 'Submit': 
            merchant_name = request.form.get('merchant_selector_dropdown') #error here, check notes. references merchant table not transactions
            amount = request.form.get('amount')
            start_date = request.form.get('start_date') 
            end_date = request.form.get('end_date')
            category_id = "13005043" #delete category from budget table 
            status= "active for storage" 

            new_budget = crud.create_budget(session.get('user_id'), merchant_name, amount, start_date, end_date, category_id, status)
            flash('New Budget Has Been Created!')
            return redirect(f'/budget/{new_budget.budget_id}')
            
        else: 
            return redirect ('/create_budget')  




@app.route('/overview', methods=['GET'])
def overview_data():
    """View transactions and account balance information"""

    if session.get('user_id'):
        user = crud.get_user_by_user_id(session['user_id'])
        return render_template('overview.html', user_name=user.user_name, transactions = user.transactions, accounts = user.accounts)
    else: 
        flash('Please login to proceed to this page.')
        return redirect('/login')    

@app.route('/overview', methods=['POST'])
def redirect_to_budgets():
    """Redirect to budgets page after clicking on button at bottom of overview page"""

    view_budgets_page = request.form.get('budgets_page')

    if  view_budgets_page == 'View My Budgets':
        return redirect('/budgets')





if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")