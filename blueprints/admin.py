from decimal import Decimal
from flask import Blueprint, flash, url_for, render_template, session, request, redirect, jsonify, current_app
from util.util import login_required, admin_required, allowed_file, changePasswordFunction, allowed_file
import db.queryStrings as QUERY
import db.db as db
import re
from werkzeug.utils import secure_filename
import os
import uuid

admin_bp = Blueprint('admin',__name__,template_folder='templates',static_folder='static', static_url_path='/blueprints/static/')

# Admin Dashboard
@admin_bp.route('/admin')
@admin_required
def admin_dashboard():

    query = QUERY.FIND_A_ADMIN_BY_ID.format(session['user_id'])
    admin_dict = db.queryOneResult(query)
    admin = list(admin_dict.values())
    customer_count = db.queryOneResult(QUERY.CUSTOMER_COUNT)['count(user_id)']
    user_count = db.queryOneResult(QUERY.USER_COUNT)['count(user_id)']
    product_count = db.queryOneResult(QUERY.PRODUCT_COUNT)['count(product_id)']
    active_product_count = db.queryOneResult(QUERY.ACTIVE_PRODUCT_COUNT)['count(product_id)']
    inactive_product_count = db.queryOneResult(QUERY.INACTIVE_PRODUCT_COUNT)['count(product_id)']
    this_month_order_count = db.queryOneResult(QUERY.CURRENT_MONTH_ORDERS_COUNT)['current_month_orders']
    last_month_order_count = db.queryOneResult(QUERY.LAST_MONTH_ORDERS_COUNT)['previous_month_orders']
    orders = db.query(QUERY.GET_ALL_ORDERS)
    shipping = db.query(QUERY.GET_ALL_SHIPPING_METHODS)
    accounts = db.query(QUERY.GET_ALL_ACCOUNTHOLDERS)
    for account in accounts:
        account['credit_used'] = db.queryOneResult(QUERY.GET_CREDIT_USED_BY_USER.format(account['user_id'])).get('credit_used')
    
    return render_template('admin/admin_dashboard.html', admin=admin,user_count=user_count, product_count=product_count,active_product_count=active_product_count, 
                           inactive_product_count=inactive_product_count, this_month_order_count=this_month_order_count, last_month_order_count=last_month_order_count,
                            orders = orders, customer_count=customer_count, shipping=shipping, accounts=accounts)

# Admin Profile
@admin_bp.route('/admin/profile')
@admin_required
def admin_profile():
    query = QUERY.GET_ADMIN_PROFILE.format(session['user_id'])
    profile = db.queryOneResult(query)
    return render_template('admin/admin_profile.html', profile = profile)

@admin_bp.route('/admin/profile/edit', methods = ['GET', 'POST'])
@admin_required
def admin_profile_edit():
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    phone = request.form.get('phone')
    if not firstName or not lastName or not phone:
        flash('Please fill in all of the fields.', 'warning')
        profile = {
            "first_name": firstName,
            "last_name": lastName,
            "phone": phone
        }
    else:
        db.query(QUERY.EDIT_ADMIN_PROFILE.format(firstName, lastName, phone ,session['user_id']))
        query = QUERY.GET_ADMIN_PROFILE.format(session['user_id'])
        profile = db.queryOneResult(query)
        session['first_name'] = firstName
        session['last_name'] = lastName
        flash('Profile updated sucssesfully.', 'success')
    return render_template('admin/admin_profile.html', profile = profile)

# Admin Users Management
@admin_bp.route('/admin/users_management', methods=['GET', 'POST'])
@admin_required
def admin_users_management():
    query = QUERY.GET_ALL_CUSTOMERS
    customers = db.query(query)
    query = QUERY.GET_ALL_STAFF
    staff = db.query(query)
 
    return render_template('admin/admin_users_management.html', customers = customers, staff=staff )

# Add New User
@admin_bp.route('/admin/admin_add_new_user', methods=['GET','POST'])
@admin_required
def admin_add_new_user():
    if request.method == 'GET':
        return render_template('admin/admin_add_new_user.html')
    else:
        user_details = {
            'user_type': request.form.get('user_type'),
            'password': request.form.get('password'),  
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email'),
        }
        account = db.queryOneResult(QUERY.FIND_A_USER_BY_EMAIL.format(user_details['email']))
        if account:
            flash('Account already exists!', 'warning')
            return redirect('/admin/users_management')
        password, salt = changePasswordFunction(user_details['password'])
        if user_details['user_type'] == 'customer':
            # Insert into users table
            id = db.querywithLastID(QUERY.REGISTER_A_NEW_USER.format(user_details['email'], password, salt ))
            # Insert into customers table
            db.query(QUERY.ADD_A_CUSTOMER.format(id,user_details['first_name'], user_details['last_name'], user_details['phone'] ))
            flash("Customer added successfully!", "success")
        elif user_details['user_type'] == 'staff':
            # Insert into users table
            id = db.querywithLastID(QUERY.REGISTER_A_NEW_USER_STAFF_TYPE.format(user_details['email'], password, salt,'staff' ))
            # Insert into staff table
            db.query(QUERY.ADD_A_STAFF.format(id,user_details['first_name'], user_details['last_name'], user_details['phone']))
            flash("Staff added successfully!", "success")
        return redirect('/admin/users_management')
    
# Deactivate a user
@admin_bp.route('/admin/users_management/deactiveUser/<int:id>')
@admin_required
def admin_deactiveUser(id):
    account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))
   
    if not account or account['user_type'] == "admin" or account['user_type'] == "manager":
        flash("Unauthorized!", 'danger')
        return redirect('/admin/users_management')
    else:
        db.queryOneResult(QUERY.DEACTIVATE_USER_BY_ID.format(id))
        flash("User is deactivated!")
        return redirect('/admin/users_management')
    

# Activate a user
@admin_bp.route('/admin/users_management/activeUser/<int:id>')
@admin_required
def admin_activeUser(id):
    account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))
    if not account or account['user_type'] == "admin" or account['user_type'] == "manager":
        flash("Unauthorized!", 'danger')
        return redirect('/admin/users_management')
    else:
        db.queryOneResult(QUERY.ACTIVATE_USER_BY_ID.format(id))
        flash("User is activated!", 'success')
        return redirect('/admin/users_management')


#edit users
@admin_bp.route('/admin/users_management/editUser/<int:id>', methods=['GET'])
@admin_required
def admin_editUser(id):

    account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))
    if not account or account['user_type'] == "manager" or account['user_type'] == "admin":
        flash("Unauthorized!", 'danger')
        return redirect('/admin/users_management')
    elif account['user_type'] == "customer":
        account = db.queryOneResult(QUERY.GET_CUSTOMER_DETAILS_BY_ID.format(id))
        return render_template('admin/admin_customer_profile.html', profile = account)
    elif account['user_type'] == "staff":
        account = db.queryOneResult(QUERY.GET_STAFF_DETAILS_BY_ID.format(id))
        return render_template('admin/admin_staff_profile.html', profile = account)
   

#edit users
@admin_bp.route('/admin/users_management/editUser/editUserDetails', methods=['POST'])
@admin_required
def admin_editUserDetails():
    
 
    id = request.form['id']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    phone = request.form['phone']
    email = request.form['email']

    account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))

    if not firstName or not lastName or not phone:
        flash('Please fill in all of the fields.', 'warning')
        return redirect('/admin/users_management/editUser/' + id)

    if email != account['email_address']:
        db.queryOneResult(QUERY.UPDATE_USER_EMAIL_BY_ID.format(email, id))

    if account['user_type'] == "customer":
        db.queryOneResult(QUERY.UPDATE_CUSTOMER_DETAILS_BY_ID.format(firstName, lastName, phone, id))
    elif account['user_type'] == "staff":
        db.queryOneResult(QUERY.UPDATE_STAFF_DETAILS_BY_ID.format(firstName, lastName, phone, id))

    flash("User profile updated!", "success")
    return redirect('/admin/users_management/editUser/' + id)


@admin_bp.route('/admin/changeUserPassword', methods=['POST'])
@admin_required
def admin_changeUserPassword():
    user_id = request.form['user_id']
    newPassword = request.form['newPassword']
    reNewPassword = request.form.get('reNewPassword')
    if newPassword != reNewPassword:
        flash("The new passwords do not match. Please try again.", 'warning')
        # Check password requirement
    elif not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}', newPassword):
        flash("The new password must contain at least 4 types and 8 characters.", 'warning')

    else:
        password, salt = changePasswordFunction(newPassword)
        db.query(QUERY.UPDATE_PASSWORD.format(password, salt, user_id))
        flash("Password updated.", 'success')

    return redirect('/admin/users_management/editUser/' + user_id)




@admin_bp.route('/admin/users_management/updateUserProfileImage', methods=['POST'])
@admin_required
def admin_updateUserProfileImage():
    if request.method == 'POST':
        id = request.form['id']

        account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))
         
        if 'image' not in request.files:
            flash('No file selected.')
           
            return redirect('/admin/users_management/editUser/' + id)
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
            if account['user_type'] == 'customer':
                role = 'Customers'
            elif account['user_type'] == 'staff':
                role = 'Staff'
            db.query(QUERY.SET_PROFILE_IMAGE.format(role, filename, id))
            session['profile_image'] = filename
            flash("Profile image updated!", "success")
        
        return redirect('/admin/users_management/editUser/' + id)
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')

@admin_bp.route('/admin/users_management/deleteUserProfileImage', methods = ['POST'])
@admin_required
def admin_deleteUserProfileImage():
    if request.method == 'POST':
        id = request.form['id']

        account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))

        query = QUERY.GET_PROFILE_IMAGE_PATH.format(id)
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
            if account['user_type'] == 'customer':
                role = 'Customers'
            elif account['user_type'] == 'staff':
                role = 'Staff'

            db.query(QUERY.DELETE_PROFILE_IMAGE.format(role, id))
            flash("Profile image deleted.", 'success')
        except Exception as e:
            flash(f"Error in deleting files: {e}", 'danger')
     
        return redirect('/admin/users_management/editUser/' + id)
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')
       
# Add and update shipping method
@admin_bp.route('/admin/shippingPriceManagement', methods=['GET','POST'])
@admin_required
def admin_shippingPriceManagement():

    if request.method == 'GET':
            query = QUERY.GET_ALL_SHIPPING_METHODS
            shipping_prices = db.query(query)
            return render_template('admin/admin_shippingPriceManagement.html', shipping_prices = shipping_prices)
    elif request.method == 'POST':
        if 'new_shipping_name' in request.form:
            new_shipping_name_raw = request.form['new_shipping_name']
            try:
                new_shipping_name = str(new_shipping_name_raw)
            except Exception as e:
                flash(f"Shipping name can only contain letters!", 'danger')
            new_shipping_price_raw = request.form['new_shipping_price']
            try:
                new_shipping_price = float(new_shipping_price_raw)
            except Exception as e:
                flash(f"Error in shipping price format: {e}", 'danger')
            db.querywithLastID(QUERY.INSERT_NEW_SHIPPING_METHOD.format(new_shipping_name, new_shipping_price))
            flash('New shipping method is added successfully!', 'success')
            return redirect(url_for('admin.admin_shippingPriceManagement'))
        else:
            shipping_name_raw = request.form['shipping_name']
            try:
                shipping_name = str(shipping_name_raw)
            except Exception as e:
                flash(f"Shipping name can only contain letters!", 'danger')
            shipping_price_raw = request.form['shipping_price']
            try:
                shipping_price = float(shipping_price_raw)
            except Exception as e:
                flash(f"Error in shipping price format: {e}", 'danger')
            shipping_method_id = request.form['shipping_method_id']

            db.querywithLastID(QUERY.UPDATE_SHIPPING_METHOD_BY_ID.format(shipping_name, shipping_price, shipping_method_id))
            flash('Selected shipping method is updated successfully!', 'success')
            return redirect(url_for('admin.admin_shippingPriceManagement'))

# Delete shopping method
@admin_bp.route('/admin/deleteShippingPrice', methods=['GET','POST'])
@admin_required
def admin_deleteShippingPrice():

        shipping_method_ids = request.form.get('selectedIds')

        if shipping_method_ids:
            query = QUERY.DELETE_SHIPPING_METHOD_BY_ID.format(shipping_method_ids)
            db.querywithLastID(query)
            flash('Selected shipping method(s) is deleted successfully!', 'success')
        return redirect(url_for('admin.admin_shippingPriceManagement'))



# Add and update categories
@admin_bp.route('/admin/categoriesManagement', methods=['GET','POST'])
@admin_required
def admin_categoriesManagement():

    if request.method == 'GET':
            query = QUERY.GET_ALL_CATEGORIES
            categories = db.query(query)
            return render_template('admin/admin_categoriesManagement.html', categories = categories)
    elif request.method == 'POST':
        if 'new_category_name' in request.form:
            new_category_name_raw = request.form['new_category_name']

            try:
                new_category_name = str(new_category_name_raw)
            except Exception as e:
                flash(f"Category name can only contain letters and numbers!", 'danger')

            db.querywithLastID(QUERY.INSERT_NEW_CATEGORY.format(new_category_name))
            flash('New category is added successfully!', 'success')
            return redirect(url_for('admin.admin_categoriesManagement'))
        else:
            category_name_raw = request.form['category_name']

            try:
                category_name = str(category_name_raw)
            except Exception as e:
                flash(f"Category name can only contain letters and numbers!", 'danger')
            category_id = request.form['category_id']

            db.querywithLastID(QUERY.UPDATE_CATEGORY_BY_ID.format(category_name, category_id))
            flash('Selected category name is updated successfully!', 'success')
            return redirect(url_for('admin.admin_categoriesManagement'))
        

# Add and update subcategories
@admin_bp.route('/admin/subcategoriesManagement', methods=['GET','POST'])
@admin_required
def admin_subcategoriesManagement():

    if request.method == 'GET':
            query = QUERY.GET_ALL_CATEGORIES_AND_SUBCATEGORIES
            categories = db.query(QUERY.GET_ALL_CATEGORIES)
            categories_and_subcategories = db.query(query)
            return render_template('admin/admin_subcategoriesManagement.html', categories_and_subcategories = categories_and_subcategories, categories=categories)
    elif request.method == 'POST':

        if 'new_subcategory_name' in request.form:
            categories_id = request.form['new_category_id']
            new_subcategory_name_raw = request.form['new_subcategory_name']

            try:
                new_subcategory_name = str(new_subcategory_name_raw)
            except Exception as e:
                flash(f"Subcategory name can only contain letters and numbers!", 'danger')

            db.querywithLastID(QUERY.INSERT_NEW_SUBCATEGORY.format(new_subcategory_name, categories_id))
            flash('New subcategory is added successfully!', 'success')
            return redirect(url_for('admin.admin_subcategoriesManagement'))
        else:
            subcategory_name_raw = request.form['subcategory_name']

            try:
                subcategory_name = str(subcategory_name_raw)
            except Exception as e:
                flash(f"Subcategory name can only contain letters and numbers!", 'danger')
            subcategory_id = request.form['subcategory_id']

            db.querywithLastID(QUERY.UPDATE_SUBCATEGORY_BY_ID.format(subcategory_name, subcategory_id))
            flash('Selected subcategory name is updated successfully!', 'success')
            return redirect(url_for('admin.admin_subcategoriesManagement'))



@admin_bp.route('/giftcard/management', methods=['GET','POST'])
@admin_required
def giftcard_list():
    if request.method == 'POST':
    # Update products quantity
      
        product_id = request.form.get('product_id')
        stock_quantity = request.form.get('stock_quantity')
        db.query(QUERY.UPDATE_PRODUCT_QUANTITY_BY_ID.format(stock_quantity, product_id))
        flash("Inventory updated successfully!", "success")
    products = db.query(QUERY.GET_GIFTCARDS_WITH_CATEGORY)
    return render_template('admin/giftcard_management.html', products = products)