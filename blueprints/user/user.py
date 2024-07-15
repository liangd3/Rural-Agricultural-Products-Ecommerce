from decimal import Decimal
from flask import Blueprint, flash, session
from flask import Blueprint,render_template,request,redirect,url_for, jsonify
from util.util import login_required, removeSession, changePasswordFunction, checkPassword, createSession
import db.queryStrings as QUERY
import db.db as db
import re
from datetime import datetime

user_bp = Blueprint('user',__name__,template_folder='templates',static_folder='static', static_url_path='/user/static/')


# Login
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    #login function here
    if request.method == 'POST':
        input_password = request.form.get('password')
        email = request.form.get('email')
        query = QUERY.FIND_A_USER_BY_EMAIL.format(email)
        account = db.queryOneResult(query)
        if not account:
            flash('Account does not exist!', 'warning')
            return redirect('/login')
        elif not checkPassword(account['password'], input_password,  account['salt']):
            flash('Wrong password!', 'danger')
            return redirect('/login')
        elif not account['user_status']:
            flash('Inactive user, please contact customer support!', 'warning')
            return redirect('/login')
        else:
            createSession(account['user_id'], email, account['user_type'] )
            if account['user_type'] == 'customer':
                flash("Login Successfully!", 'success')
                customer = db.queryOneResult(QUERY.GET_CUSTOMER_PROFILE.format(account['user_id']))
                
                session['credit_limit'] = float(customer['credit_limit'])
                return redirect('/customer')
            elif account['user_type'] == 'staff':
                flash("Login Successfully!", 'success')
                return redirect('/staff')
            elif account['user_type'] == 'manager':
                flash("Login Successfully!", 'success')
                return redirect('/manager')
            elif account['user_type'] == 'admin':
                flash("Login Successfully!", 'success')
                return redirect('/admin')
    return render_template('login.html' )

# Registration
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    #register function here
    if request.method == 'POST':
        input_password = request.form.get('password')
        email = request.form.get('email')
        query = QUERY.FIND_A_USER_BY_EMAIL.format(email)
        account = db.queryOneResult(query)
        if account:
            flash('Account already exists!', 'warning')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'warning')
        elif not input_password or not email:
            flash('Please fill out the form!', 'warning')
        elif not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W])(?!.*\s).{8,}$', input_password):
            flash('Password must be minimum eight characters, one uppercase letter, one lowercase letterone number and one special character!', 'warning')
        else:
            password, salt = changePasswordFunction(input_password)
            query = QUERY.REGISTER_A_NEW_USER.format(email,password, salt )
            id = db.querywithLastID(query)
            none_credit = 0.00
            db.query( QUERY.REGISTER_A_NEW_CUSTOMER.format(id, datetime.today(), none_credit))
            flash('You have successfully registered!', 'success')
            return redirect('/login')
    return render_template('register.html')


# Logout
@user_bp.route('/logout')
def logout():
#    print('{timestamp} -- logout request started'.format(timestamp=datetime.utcnow().isoformat()))
   removeSession()
#    print('{timestamp} -- logout request ended'.format(timestamp=datetime.utcnow().isoformat()))
   return redirect('/')


# Route to check email availability
@user_bp.route('/check_email', methods=['POST'])
def check_email():
    if 'email' in request.json:
        email = request.json['email']
        query = QUERY.FIND_A_USER_BY_EMAIL.format(email)
        account = db.query(query)
        return jsonify({"exists": True if account else False})
    return jsonify({"exists": False})  # Return false if email is not provided in request

