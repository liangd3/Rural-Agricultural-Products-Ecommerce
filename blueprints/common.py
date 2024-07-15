from flask import Blueprint, flash,render_template,request,redirect, session,url_for, jsonify, current_app
from datetime import datetime, timedelta
import db.queryStrings as QUERY
import db.db as db
from util.util import login_required, checkPassword, uploadImage, changePasswordFunction, allowed_file, updatePromotionStatus, level_one_required, get_price_after_discount
import re
import os
from werkzeug.utils import secure_filename
import uuid


common_bp = Blueprint('common',__name__,template_folder='templates',static_folder='static', static_url_path='/blueprints/static/')

# Home Page
@common_bp.route('/')
@common_bp.route('/home')
def home():
    updatePromotionStatus()

    if 'loggedin' in session:
        if session['user_type'] == 'customer':
            return redirect(url_for('customer.customer_dashboard'))
    #     elif session['user_type'] == 'staff':
    #         return redirect(url_for('staff.staff_dashboard'))
    #     elif session['user_type'] == 'manager':
    #         return redirect(url_for('manager.manager_dashboard'))
    #     elif session['user_type'] == 'admin':
    #         return redirect(url_for('admin.admin_dashboard'))
    categories = db.query(QUERY.GET_ALL_CATEGORIES)
    subcategories = db.query(QUERY.GET_ALL_SUBCATEGORIES)
    promotions = db.query(QUERY.GET_PROMOTION_LIST)

    hot_products = db.query(QUERY.GET_HOT_PRODUCTS)
    news = db.query(QUERY.GET_ALL_NEWS)

    return render_template('home.html',  hot_products=hot_products, promotions=promotions, news=news,  categories = categories,subcategories = subcategories )

@common_bp.route('/<role>/password/update', methods = ['GET', 'POST'])
@login_required
def password_update(role):
    if request.method == 'POST':
        currentPassword = request.form.get('currentPassword')
        newPassword = request.form.get('newPassword')
        reNewPassword = request.form.get('reNewPassword')

        query = QUERY.GET_CURRENT_PASSWORD.format(session['user_id'])
        account = db.queryOneResult(query)

        # Check current password is correct
        if not checkPassword(account['password'], currentPassword, account['salt']):
            flash("The current password does not match.", 'warning')
        # Compare the two new password input
        elif newPassword != reNewPassword:
            flash("The new passwords do not match. Please try again.", 'warning')
        # Check password requirement
        elif not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}', newPassword):
            flash("The new password must contain at least 4 types and 8 characters.", 'warning')
        # Update Password
        else:
            password, salt = changePasswordFunction(newPassword)
            db.query(QUERY.UPDATE_PASSWORD.format(password, salt, session['user_id']))
            flash("Password updated.", 'success')

        path = f"{role}.{role}_profile"
        return redirect(url_for(path))
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')

@common_bp.route('/<role>/profile/uploader', methods = ['GET', 'POST'])
@login_required
def profile_picture_upload(role):
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file selected.')
            path = f"{role}.{role}_profile"
            return redirect(url_for(path))
        file = request.files['image']
        if file.filename == '':
            flash('No file uploaded.')
        elif file and allowed_file(file.filename):
            UPLOAD_FOLDER = 'static/profile_image'
            current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            filename = secure_filename(file.filename)
            
            index = filename.rfind('.')
            substring = filename[index:]
            filename = uuid.uuid4().hex + substring

            basedir = os.path.abspath(os.path.dirname(__file__))
            filePath = basedir + "/" + UPLOAD_FOLDER
            if not os.path.exists(filePath):
                os.makedirs(filePath)
            file.save(os.path.join(basedir, UPLOAD_FOLDER, filename))

            # change blueprint name style to table name style
            roles = role
    
            if role == "staff": 
                roles = 'Staff'
            elif role == "customer": 
                roles = "Customers"
            elif role == "admin": 
                roles = "Admins"
            elif role == "manager": 
                roles = "Managers"

            db.query(QUERY.SET_PROFILE_IMAGE.format(roles, filename, session['user_id']))
            session['profile_image'] = filename
            flash('Image uploaded.', 'success')
        path = f"{role}.{role}_profile" 
        return redirect(url_for(path))
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')

@common_bp.route('/<role>/profile/delete', methods = ['GET', 'POST'])
@login_required
def profile_picture_delete(role):
    if request.method == 'POST':
        query = QUERY.GET_PROFILE_IMAGE_PATH.format(session['user_id'])
        file = db.queryOneResult(query)
        try:
            UPLOAD_FOLDER = 'static/profile_image'
            current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
           

            basedir = os.path.abspath(os.path.dirname(__file__))
            filePath = basedir + "/" + UPLOAD_FOLDER
            if not os.path.exists(filePath):
                os.makedirs(filePath)
         
    
            os.remove(os.path.join(basedir, UPLOAD_FOLDER, file['profile_image']))

            # change blueprint name style to table name style
            roles = role
            if role == "staff": 
                roles = 'Staff'
            elif role == "customer": 
                roles = "Customers"
            elif role == "admin": 
                roles = "Admins"
            elif role == "manager": 
                roles = "Managers"


            db.query(QUERY.DELETE_PROFILE_IMAGE.format(roles, session['user_id']))
            flash("Profile image deleted.", 'success')
        except Exception as e:
            flash(f"Error in deleting files: {e}", 'danger')
        path = f"{role}.{role}_profile" 
        return redirect(url_for(path))
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')
    


# Contact us Page
@common_bp.route('/contactus')
def contactUs():
    return render_template('contactUs.html')