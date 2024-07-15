from flask import Blueprint, flash, url_for, render_template, session, request, redirect, current_app
from util.util import login_required, manager_required, allowed_file, updatePromotionStatus, changePasswordFunction, level_two_required, sendMessage
from app import *
import db.queryStrings as QUERY
import db.db as db
import re
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import date

manager_bp = Blueprint('manager',__name__,template_folder='templates',static_folder='static', static_url_path='/blueprints/static/')


# Manager Dashboard

@manager_bp.route('/manager', methods =  ['GET', 'POST'])
@manager_required
def manager_dashboard():
    customer_count = db.queryOneResult(QUERY.CUSTOMER_COUNT)['count(user_id)']
    this_month_order_count = db.queryOneResult(QUERY.CURRENT_MONTH_ORDERS_COUNT)['current_month_orders']
    last_month_order_count = db.queryOneResult(QUERY.LAST_MONTH_ORDERS_COUNT)['previous_month_orders']
    new_message_count = db.queryOneResult(QUERY.NEW_MESSAGE_COUNT)['count(message_id)']
    new_application_count = db.queryOneResult(QUERY.NEW_APPLICATION_COUNT)['application_count']

    if request.method == 'POST':

        user_id = request.form.get('user_id')
        message_subject = 'Payment overdue'
        orders = db.query(QUERY.GET_CUSTOMER_OVERDUE_ORDERS.format(user_id))
        message_content = 'You have overdue orders, including:'
        for o in orders:
            message_content += 'Order ID: ' + str(o['order_id']) + ', Ordered on: ' + o['order_date'].strftime('%d/%m/%Y') + ', Amount: $' + str(o['total_amount'])

        sendMessage(user_id, message_subject, message_content)
        flash('Reminder sent!', 'success')
            
    payments = db.query(QUERY.GET_CUSTOMERS_OVERDUE_PAYMENT)
    product_sales_data = db.query(QUERY.PRODUCT_SALES_DATA)

    return render_template('manager/manager_dashboard.html',customer_count=customer_count, 
                           new_message_count=new_message_count, this_month_order_count=this_month_order_count, last_month_order_count=last_month_order_count, 
                           new_application_count=new_application_count, payments = payments,product_sales_data=product_sales_data)

# Manager Profile
@manager_bp.route('/manager/profile')
@manager_required
def manager_profile():
    profile = db.queryOneResult(QUERY.GET_MANAGER_PROFILE.format(session['user_id']))
    return render_template('manager/manager_profile.html', profile = profile)

@manager_bp.route('/manager/profile/edit', methods = ['GET', 'POST'])
@manager_required
def manager_profile_edit():
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    phone = request.form.get('phone')
    if not firstName or not lastName or not phone:
        flash('Please fill in all of the fields.','warning')
        profile = {
            "first_name": firstName,
            "last_name": lastName,
            "phone": phone
        }
    else:
        db.query(QUERY.EDIT_MANAGER_PROFILE.format(firstName, lastName, phone ,session['user_id']))
        query = QUERY.GET_MANAGER_PROFILE.format(session['user_id'])
        profile = db.queryOneResult(query)
        session['first_name'] = firstName
        session['last_name'] = lastName
        flash('Profile updated sucssesfully.', 'success')
    return render_template('manager/manager_profile.html', profile = profile)

# Manager Users Management
@manager_bp.route('/manager/users_management', methods=['GET'])
@manager_required
def manager_users_management():
    query = QUERY.GET_ALL_CUSTOMERS
    customers = db.query(query)
    query = QUERY.GET_ALL_STAFF
    staff = db.query(query)
    return render_template('manager/manager_users_management.html', customers = customers, staff=staff)

# Add New User
@manager_bp.route('/manager/manager_add_new_user', methods=['GET','POST'])
@manager_required
def manager_add_new_user():
    if request.method == 'GET':
        return render_template('manager/manager_add_new_user.html')
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
            return redirect('/manager/users_management')
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
        return redirect('/manager/users_management')


#edit users
@manager_bp.route('/manager/users_management/editUser/<int:id>', methods=['GET'])
@manager_required
def manager_editUser(id):

    account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))
    if not account or account['user_type'] == "manager" or account['user_type'] == "admin":
        flash("Unauthorized!", 'danger')
        return redirect('/manager/users_management')
    elif account['user_type'] == "customer":
        account = db.queryOneResult(QUERY.GET_CUSTOMER_DETAILS_BY_ID.format(id))
        return render_template('manager/manager_customer_profile.html', profile = account)
    elif account['user_type'] == "staff":
        account = db.queryOneResult(QUERY.GET_STAFF_DETAILS_BY_ID.format(id))
        return render_template('manager/manager_staff_profile.html', profile = account)
   

#edit users
@manager_bp.route('/manager/users_management/editUser/editUserDetails', methods=['POST'])
@manager_required
def manager_editUserDetails():
  
 
    id = request.form['id']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    phone = request.form['phone']
    email = request.form['email']

    account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))

    if not firstName or not lastName or not phone:
        flash('Please fill in all of the fields.', 'warning')
        return redirect('/manager/users_management/editUser/' + id)

    if email != account['email_address']:
        db.queryOneResult(QUERY.UPDATE_USER_EMAIL_BY_ID.format(email, id))

    if account['user_type'] == "customer":
        db.queryOneResult(QUERY.UPDATE_CUSTOMER_DETAILS_BY_ID.format(firstName, lastName, phone, id))
    elif account['user_type'] == "staff":
        db.queryOneResult(QUERY.UPDATE_STAFF_DETAILS_BY_ID.format(firstName, lastName, phone, id))

    flash("User profile updated!", "success")
    return redirect('/manager/users_management/editUser/' + id)


# Deactivate a user
@manager_bp.route('/manager/users_management/deactiveUser/<int:id>')
@manager_required
def manager_deactiveUser(id):
    account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))
   
    if not account or account['user_type'] == "manager" or account['user_type'] == "admin":
        flash("Unauthorized!", 'danger')
        return redirect('/manager/users_management')
    else:
        db.queryOneResult(QUERY.DEACTIVATE_USER_BY_ID.format(id))
        flash("User is deactivated!")
        return redirect('/manager/users_management')

# Activate a user
@manager_bp.route('/manager/users_management/activeUser/<int:id>')
@manager_required
def manager_activeUser(id):
    account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))
    if not account or account['user_type'] == "manager" or account['user_type'] == "admin":
        flash("Unauthorized!", 'danger')
        return redirect('/manager/users_management')
    else:
        db.queryOneResult(QUERY.ACTIVATE_USER_BY_ID.format(id))
        flash("User is activated!", 'success')
        return redirect('/manager/users_management')


# Manager Promotion Management
@manager_bp.route('/promotion_management')
@level_two_required
def manager_promotion_management():
    updatePromotionStatus()
    promotions = db.query(QUERY.GET_PROMOTION_LIST.format())
    return render_template('manager/promotion_manage.html', promotions = promotions )

@manager_bp.route('/promotion_management/sort', methods=['POST'])
@level_two_required
def promotion_list_sorted():
    updatePromotionStatus()
    type = request.form.get('type')
    status = request.form.get('status')
    print(type, status)

    typeQ = f'promotion_type = "{type}"' if type else ''
    statusQ = f'status = "{status}"' if status else ''
    andQ = 'AND' if typeQ and statusQ else ''
    
    promotions = db.query(f'SELECT * FROM Promotions WHERE {typeQ} {andQ} {statusQ} ORDER BY promotion_id ASC;')
    return render_template('manager/promotion_manage.html', promotions = promotions, type = type, status = status)


@manager_bp.route('/promotion/<int:id>')
@level_two_required
def promotion_detail(id):
    updatePromotionStatus()
    promotion = db.queryOneResult(QUERY.GET_PROMOTION_DETAIL.format(id))
    categories = db.query(QUERY.GET_PROMOTION_CATAGORIES.format(id))
    subcategories = db.query(QUERY.GET_PROMOTION_SUBCATAGORIES.format(id))
    products = db.query(QUERY.GET_PROMOTION_PRODUCTS.format(id))
    allCategories = db.query(QUERY.GET_ALL_CATEGORIES_EXCLUDES_GIFTCARD.format())
    allSubcategories = db.query(QUERY.GET_ALL_SUBCATEGORIES_EXCLUDES_GIFTCARD.format())
    allProducts = db.query(QUERY.GET_ALL_PRODUCTS_EXCLUDES_GIFTCARD.format())
    return render_template('manager/promotion_detail.html', promotion = promotion, categories = categories, subcategories = subcategories, products = products, allCategories = allCategories, allSubcategories = allSubcategories, allProducts = allProducts)

@manager_bp.route('/promotion/<int:id>/edit_submit', methods=['POST','GET'])
@level_two_required
def promotion_edit(id):
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        type = request.form.get('type')
        discountType = request.form.get('discount_type')
        discount = request.form.get('discount')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        discountType = discountType if discountType != "rate" else None
        discount = request.form.get('discount') if discountType == "rate" else 0

        # convert discount to decimal
        discount = str(int(discount) / 100)

        # check current type
        currentType = db.queryOneResult(QUERY.GET_PROMOTION_TYPE.format(id))
        if type != currentType['Promotion_type']:
            db.query(QUERY.CLEAR_PROMOTION_ITEM.format("Categories", id))
            db.query(QUERY.CLEAR_PROMOTION_ITEM.format("Subcategories", id))
            db.query(QUERY.CLEAR_PROMOTION_ITEM.format("Products", id))
        db.query(QUERY.UPDATE_PROMOTION.format(name, description, type, discount, discountType, start_date, end_date, id))
        flash(f'Promotion {name} updated.', 'success')
    return redirect(url_for('manager.promotion_detail', id=id))

@manager_bp.route('/promotion/<int:id>/delete', methods=['POST','GET'])
@level_two_required
def promotion_delete(id):
    if request.method == "POST":
        db.query(QUERY.DELETE_PROMOTION.format(id))
        flash(f'Promotion #{id} deleted.', 'success')
    return redirect(url_for('manager.manager_promotion_management'))
    

@manager_bp.route('/promotion/<int:id>/<type>/submit', methods=['POST','GET'])
@level_two_required
def promotion_type_edit(id, type):
    if request.method == "POST":
        promotionItems = request.form.getlist('itemsChecked')

        # Convert to db table name
        if type == "category":
            table = "Categories"
        elif type == "subcategory":
            table = "Subcategories"
        elif type == "product":
            table = "Products"
        
        db.query(QUERY.CLEAR_PROMOTION_ITEM.format(table, id))
        for item in promotionItems:
            db.query(QUERY.UPDATE_PROMOTION_ITEM.format(table, id, item))
        flash(f'Items in Promotion #{id} updated.', 'success')
    return redirect(url_for('manager.promotion_detail', id=id))

@manager_bp.route('/promotion/<int:id>/uploader', methods = ['GET', 'POST'])
@login_required
def profile_picture_upload(id):
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file selected.')
            return redirect(url_for('manager.promotion_detail', id=id))
        file = request.files['image']
        if file.filename == '':
            flash('No file uploaded.')
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('/home/arproject2/COMP639S1_Project_2_Group_AR/static/promotion_image', filename))
            db.query(QUERY.UPDATE_PROMOTION_IMAGE.format(file.filename, id))
            session['profile_image'] = filename
            flash('Image uploaded.', 'success')
        return redirect(url_for('manager.promotion_detail', id=id))
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')

@manager_bp.route('/manager/promotion/<int:id>/delete', methods = ['GET', 'POST'])
@login_required
def profile_picture_delete(id):
    if request.method == 'POST':
        file = db.queryOneResult(QUERY.GET_PROMOTION_IMAGE_PATH.format(id))
        try:
            os.remove(os.path.join('static', 'promotion_image', file['promotion_image']))
            db.query(QUERY.DELETE_PROMOTION_IMAGE.format(id))
            flash("Promotion image deleted.", 'success')
        except Exception as e:
            flash(f"Error in deleting files: {e}", 'danger')
        return redirect(url_for('manager.promotion_detail', id=id))
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')

@manager_bp.route('/manager/promotion/new', methods = ['GET', 'POST'])
@level_two_required
def promotion_new():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        type = request.form.get('type')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        discountType = request.form.get('discount_type')

        discountType = discountType if discountType != "rate" else None
        discount = request.form.get('discount') if discountType == "rate" else 0

        getPromotionItems = type + "Checked"
        promotionItems = request.form.getlist(getPromotionItems)

        # convert discount to decimal
        discount = str(int(discount) / 100)

        id = db.querywithLastID(QUERY.NEW_PROMOTION.format(name, description, type, discount, discountType, start_date, end_date))

        # Convert to db table name
        if type == "category":
            table = "Categories"
        elif type == "subcategory":
            table = "Subcategories"
        elif type == "product":
            table = "Products"
        
        db.query(QUERY.CLEAR_PROMOTION_ITEM.format(table, id))
        for item in promotionItems:
            db.query(QUERY.UPDATE_PROMOTION_ITEM.format(table, id, item))

        flash(f'Promotion {name} added.', 'success')
        return redirect(url_for('manager.promotion_detail', id=id))

    else:
        allCategories = db.query(QUERY.GET_ALL_CATEGORIES.format())
        allSubcategories = db.query(QUERY.GET_ALL_SUBCATEGORIES.format())
        allProducts = db.query(QUERY.GET_ALL_PRODUCTS.format())
        return render_template('manager/promotion_new.html', allCategories = allCategories, allSubcategories = allSubcategories, allProducts = allProducts )



@manager_bp.route('/manager/users_management/updateUserProfileImage', methods=['POST'])
@level_two_required
def manager_updateUserProfileImage():
    if request.method == 'POST':
        id = request.form['id']

        account = db.queryOneResult(QUERY.FIND_A_USER_BY_ID.format(id))
         
        if 'image' not in request.files:
            flash('No file selected.')
           
            return redirect('/manager/users_management/editUser/' + id)
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
        
        return redirect('/manager/users_management/editUser/' + id)
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')

@manager_bp.route('/manager/users_management/deleteUserProfileImage', methods = ['POST'])
@level_two_required
def manager_deleteUserProfileImage():
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
     
        return redirect('/manager/users_management/editUser/' + id)
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')
       



@manager_bp.route('/reward/management', methods =  ['GET', 'POST'])
@level_two_required
def rewardManagement():
    points = db.query(QUERY.GET_REWARD_POINTS)
   
    highest_customer_point = db.queryOneResult(QUERY.GET_MAX_CUSTOMER_POINT)
    highest_customer_point = highest_customer_point['p']

    highest_reward_point = db.queryOneResult(QUERY.GET_MAX_REWARD_POINTS)
    highest_reward_point = highest_reward_point['p']

    if request.method == 'POST':
        level_point = int(request.form.get('level_point'))
        gift_card_amount = request.form.get('gift_card_amount')
        if level_point > highest_reward_point:
            db.query(QUERY.SET_NEW_REWARD_POINTS.format(level_point, gift_card_amount))
            flash('New Level Set Success!', 'success')
            return redirect('/reward/management')

    return render_template('manager/reward_management.html', points = points, highest_customer_point = highest_customer_point,  highest_reward_point = highest_reward_point, higher = max(highest_customer_point, highest_reward_point) )
       



@manager_bp.route('/reward/management/delete', methods =  ['POST'])
@level_two_required
def rewardManagementDelete():
    if request.method == 'POST':
        level_id = request.form.get('level_id')
        
        db.query(QUERY.DELETE_REWARD_LEVEL.format(level_id))
        flash('Delete Success!', 'success')

    return redirect('/reward/management')




@manager_bp.route('/accountholder/management', methods = ['GET', 'POST'])
@level_two_required
def accountholderManagement():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        credit_limit = request.form.get('credit_limit')
        db.query(QUERY.UPDATE_ACCOUNTHOLDER_CREDIT_LIMIT.format(credit_limit, user_id))
        flash('Credit update Success!', 'success')

    accounts = db.query(QUERY.GET_ALL_ACCOUNTHOLDERS)
    for account in accounts:
        account['credit_used'] = db.queryOneResult(QUERY.GET_CREDIT_USED_BY_USER.format(account['user_id'])).get('credit_used')
        
    return render_template('manager/accountholder_management.html', accounts = accounts )

@manager_bp.route('/payment/management', methods =  ['GET', 'POST'])
@level_two_required
def paymentManagement():
    if request.method == 'POST':

            user_id = request.form.get('user_id')
            message_subject = 'Payment overdue'
            orders = db.query(QUERY.GET_CUSTOMER_OVERDUE_ORDERS.format(user_id))
            message_content = 'You have overdue orders, including:'
            for o in orders:
                message_content += 'Order ID: ' + str(o['order_id']) + ', Ordered on: ' + o['order_date'].strftime('%d/%m/%Y') + ', Amount: $' + str(o['total_amount'])

            sendMessage(user_id, message_subject, message_content)
            flash('Reminder sent!', 'success')
            
    payments = db.query(QUERY.GET_CUSTOMERS_OVERDUE_PAYMENT)

    return render_template('manager/payment_management.html', payments = payments)


# View all news
@manager_bp.route('/newsManagement', methods=['GET','POST'])
@level_two_required
def newsManagement():
    query = QUERY.GET_ALL_NEWS
    news = db.query(query)
    return render_template('news/newsManagement.html', news = news)

# Edit a news
@manager_bp.route('/newsManagement/<int:id>',methods = ['GET', 'POST'])
@level_two_required
def news_detail(id):
    if request.method == 'POST':
            sender_id = session['user_id']
            news_subject = request.form['news_subject']
            news_content = request.form['news_content']
        
            db.querywithLastID(QUERY.UPDATE_NEWS_BY_ID.format(sender_id, news_subject, news_content, id))

            if 'uploadInputFile' in request.files:
                file = request.files['uploadInputFile']
                if file and allowed_file(file.filename):
                    UPLOAD_FOLDER = 'static/news'
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
                    db.querywithLastID(QUERY.UPDATE_NEWS_IMAGE.format(filename, id))
            flash('Selected news is updated successfully!', 'success')

    new = db.queryOneResult(QUERY.GET_NEWS_BY_ID.format(id))

    return render_template('news/news_detail.html', new=new)

# Send news
@manager_bp.route('/newsManagement/<int:id>/<action>',methods = ['POST'])
@level_two_required
def sendNews(id, action):
    if action == "sent":
        sender_id = session['user_id']
        db.query(QUERY.SEND_NEWS_BY_ID.format(sender_id, id))
        flash('Selected news is sent successfully!', 'success')

    return redirect(url_for('manager.news_detail', id = id))

# Add new news
@manager_bp.route('/newsManagement/new', methods=['GET', 'POST'])
@level_two_required
def addNews():
    if request.method == 'POST':
        sender_id = 3
        news_subject = request.form['news_subject']
        news_content = request.form['news_content']
        news_timestamp = datetime.now()


        if 'uploadInputFile' in request.files:
                file = request.files['uploadInputFile']

                if file and allowed_file(file.filename):
                    UPLOAD_FOLDER = 'static/news'
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
                    # db.querywithLastID(QUERY.INSERT_NEW_NEWS_IMAGE.format(filename))

        db.querywithLastID(QUERY.ADD_NEW_NEWS.format(sender_id, news_subject, news_content, filename, news_timestamp))
        flash('New news is added.', 'success')
        return redirect(url_for('manager.newsManagement'))
    return render_template('news/newNews.html')

# Upload new news image
@manager_bp.route('/newsManagement/<int:id>/uploader', methods=['GET', 'POST'])
@level_two_required
def news_img_uploader(id):
    if request.method == 'POST':
        if 'uploadedImage' in request.files:
            file = request.files['uploadedImage']

            if file and allowed_file(file.filename):
                UPLOAD_FOLDER = 'static/news'
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
                db.querywithLastID(QUERY.UPDATE_NEWS_IMAGE_BY_ID.format(filename, id))
            
            flash('News image upoaded.', 'success')
    return redirect(url_for('manager.news_detail', id = id))

# Delete news image
@manager_bp.route('/newsManagement/<int:newsID>/image/delete', methods=['GET', 'POST'])
@level_two_required
def news_img_delete(newsID):
    if request.method == 'POST':
        file = db.queryOneResult(QUERY.GET_NEWS_BY_ID.format(newsID))
        try:
            db.query(QUERY.UPDATE_NEWS_IMAGE_TO_NULL.format(newsID))

            UPLOAD_FOLDER = 'static/news'
            current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
           

            basedir = os.path.abspath(os.path.dirname(__file__))
            filePath = basedir + "/" + UPLOAD_FOLDER
            if not os.path.exists(filePath):
                os.makedirs(filePath)
         
            os.remove(os.path.join(basedir, UPLOAD_FOLDER, file['news_image']))
               
            flash("News image is deleted.", 'success')
        except Exception as e:
           
            flash(f"Error in deleting files: {e}", 'danger')
     
        return redirect(url_for('manager.news_detail', id = newsID))
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')
    
# Delete news
@manager_bp.route('/newsManagement/deleteNews', methods=['GET','POST'])
@level_two_required
def deleteNews():

        news_ids = request.form.get('selectedIds')

        if news_ids:
            db.querywithLastID(QUERY.DELETE_NEWS_BY_ID.format(news_ids))
            flash('Selected news is deleted successfully!', 'success')
        return redirect(url_for('manager.newsManagement'))



@manager_bp.route('/reports', methods =  ['GET','POST'])
@level_two_required
def reports():
    today = date.today()
    if request.method == 'POST':
        startdate = request.form.get('startdate')
        enddate = request.form.get('enddate')
        if not enddate:
            enddate = today
        products = db.query(QUERY.PRODUCTS_REPORT_GIVEN_DATE.format(startdate, enddate))
        customers =  db.query(QUERY.CUSTOMERS_REPORT_GIVEN_DATE.format(startdate, enddate))
        orders = db.query(QUERY.ORDERS_REPORT_GIVEN_DATE.format(startdate, enddate))
      
    else: 
        products = db.query(QUERY.PRODUCTS_REPORT)
        customers =  db.query(QUERY.CUSTOMERS_REPORT)
        orders = db.query(QUERY.ORDERS_REPORT)
        startdate = None
        enddate = None
    
    return render_template('manager/reports.html', products = products, customers = customers, orders = orders , today = today, startdate = startdate, enddate = enddate )


# View all reviews
@manager_bp.route('/reviews', methods=['GET','POST'])
@level_two_required
def reviewsManagement():

    reviews = db.query(QUERY.GET_ALL_REVIEWS_WITH_PRODUCT_IMAGES)
    return render_template('reviews/reviewsManagement.html', reviews = reviews)

# Hide a review
@manager_bp.route('/reviews/hideReview', methods=['POST'])
@level_two_required
def hideReview():

    review_id = request.form.get('selectedId')

    if review_id:
        db.querywithLastID(QUERY.HIDE_A_REVIEW.format(review_id))
        flash('Selected review is hided successfully!', 'success')
    return redirect(url_for('manager.reviewsManagement'))

# Show a review
@manager_bp.route('/reviews/showReview', methods=['POST'])
@level_two_required
def showReview():

    review_id = request.form.get('selectedReviewId')

    if review_id:
        db.querywithLastID(QUERY.SHOW_A_REVIEW.format(review_id))
        flash('Selected review is showing now!', 'success')
    return redirect(url_for('manager.reviewsManagement'))



@manager_bp.route('/customerorders/<int:id>', methods=['GET'])
@level_two_required
def customerorders(id):
    customer =  db.queryOneResult(QUERY.GET_CUSTOMER_PROFILE.format(id))
    orders = db.query(QUERY.GET_ALL_ORDERS_BY_CUSTOMER_ID.format(id))
    return render_template('manager/customerorders.html', customer = customer, orders = orders)