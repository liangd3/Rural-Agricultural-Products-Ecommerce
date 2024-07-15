from decimal import Decimal
from flask import Blueprint, flash
from flask import Blueprint,render_template,request,redirect,url_for, jsonify, session, current_app
from util.util import login_required, removeSession, changePasswordFunction, checkPassword, createSession, level_one_required, level_two_required,allowed_file, sendMessage, updateCustomerPoints, generateGiftCard
import db.queryStrings as QUERY
import db.db as db
import re
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import uuid



internal_bp = Blueprint('internal',__name__,template_folder='templates',static_folder='static', static_url_path='/blueprints/static/')


@internal_bp.route('/inventory', methods=['GET','POST'])
@level_one_required
def inventory_list():
    if request.method == 'POST':
    # Update products quantity
      
        product_id = request.form.get('product_id')
        stock_quantity = request.form.get('stock_quantity')
        db.query(QUERY.UPDATE_PRODUCT_QUANTITY_BY_ID.format(stock_quantity, product_id))
        flash("Inventory updated successfully!", "success")
    products = db.query(QUERY.GET_ALL_PRODUCTS_WITH_CATEGORY)
    return render_template('inventory/inventory_management.html', products = products)

# Edit a product detail
@internal_bp.route('/inventory/<int:id>',methods = ['GET', 'POST'])
@level_one_required
def product_detail(id):
    if request.method == 'POST':
        product_name = request.form.get('name')
        product_description = request.form.get('description')
        product_price = request.form.get('price')
        subcategory_id = request.form.get('subcategory')
        stock_quantity = request.form.get('quantity')
        oversized = request.form.get('oversized')
        
        db.query(QUERY.UPDATE_PRODUCT_DETAIL_BY_ID.format(product_name, product_description, product_price, subcategory_id,oversized,  stock_quantity, id))
        if 'uploadInputFile' in request.files:
            file = request.files['uploadInputFile']
            if file and allowed_file(file.filename):
                UPLOAD_FOLDER = 'static/product_image'
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
                imageID = db.querywithLastID(QUERY.INSERT_NEW_PRODUCT_IMAGE.format(filename, id))
                primaryImage = db.queryOneResult(QUERY.CHECK_PRODUCT_PRIMARY_IMAGE_BY_ID.format(id))
                if not primaryImage:
                    db.query(QUERY.UPDATE_PRODUCT_PRIMARY_IMAGE.format(imageID, id))

        flash('Product detail updated.', 'success')

    product = db.queryOneResult(QUERY.GET_PRODUCT_DATAILS_BY_ID.format(id))
    images = db.query(QUERY.GET_PRODUCT_IMAGES_BY_ID.format(id))

    allCategories = db.query(QUERY.GET_ALL_CATEGORIES)
    allSubcategories = db.query(QUERY.GET_ALL_SUBCATEGORIES)


    return render_template('/inventory/product_detail.html', product = product, images = images , allSubcategories = allSubcategories, allCategories = allCategories)

# Change a product status
@internal_bp.route('/inventory/<int:id>/<action>',methods = ['POST'])
@level_one_required
def product_status(id, action):
    if action == "inactivate":
        db.query(QUERY.INACTIVATE_A_PRODUCT_BY_ID.format(id))
    else:
        db.query(QUERY.ACTIVATE_A_PRODUCT_BY_ID.format(id))
    return redirect(url_for('internal.product_detail', id = id))

@internal_bp.route('/inventory/new', methods=['GET', 'POST'])
@level_one_required
def addProduct():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        subcategory = request.form.get('subcategory')
        quantity = request.form.get('quantity')
        oversized = request.form.get('oversized')

        subcategoryID = db.queryOneResult(QUERY.GET_SUBCAT_ID_FROM_NAME.format(subcategory))
        productID = db.querywithLastID(QUERY.INSERT_PRODUCT.format(name, description, price, subcategoryID['subcategory_id'], quantity, oversized))

        if 'uploadInputFile' in request.files:
            files = request.files.getlist('uploadInputFile')
            if len(files) > 5:
                flash('Product added but maximum of 5 images exceeded. Please try again.','warning')
                return redirect(url_for('internal.product_detail', id = productID))

            for file in files:
                if file and allowed_file(file.filename):
                    UPLOAD_FOLDER = 'static/product_image'
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
                    imageID = db.querywithLastID(QUERY.INSERT_NEW_PRODUCT_IMAGE.format(filename, productID))
                    primaryImage = db.queryOneResult(QUERY.CHECK_PRODUCT_PRIMARY_IMAGE_BY_ID.format(productID))
                    print(primaryImage)
                    if not primaryImage or not primaryImage['product_image_id']:
                        db.query(QUERY.UPDATE_PRODUCT_PRIMARY_IMAGE.format(imageID, productID))
        flash('Product added.', 'success')
        return redirect(url_for('internal.inventory_list'))
    allCategories = db.query(QUERY.GET_ALL_CATEGORIES.format())
    return render_template('inventory/product_new.html', allCategories = allCategories)

@internal_bp.route('/inventory/<int:id>/uploader', methods=['GET', 'POST'])
@level_one_required
def product_img_uploader(id):
    if request.method == 'POST':
        if 'uploadedImages' in request.files:
            files = request.files.getlist('uploadedImages')
            currentFileCount = db.queryOneResult(QUERY.GET_PRODUCT_IMAGE_COUNT.format(id))

            if currentFileCount['count'] + len(files) > 5:
                remaining = 5 - currentFileCount['count'] - len(files)
                flash(f'Only {remaining} more files can be uploaded.', 'warning')
                return redirect(url_for('internal.product_detail', id = id))

            for file in files:
                if file and allowed_file(file.filename):
                    UPLOAD_FOLDER = 'static/product_image'
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
                    imageID = db.querywithLastID(QUERY.INSERT_NEW_PRODUCT_IMAGE.format(filename, id))
                    primaryImage = db.queryOneResult(QUERY.CHECK_PRODUCT_PRIMARY_IMAGE_BY_ID.format(id))
                    if not primaryImage:
                        db.query(QUERY.UPDATE_PRODUCT_PRIMARY_IMAGE.format(imageID, id))
            
            flash('Image upoaded.', 'success')
    return redirect(url_for('internal.product_detail', id = id))

@internal_bp.route('/inventory/<int:productID>/image/<int:imageID>/delete', methods=['GET', 'POST'])
@level_one_required
def product_img_delete(productID, imageID):
    if request.method == 'POST':
        file = db.queryOneResult(QUERY.GET_PRODUCT_IMAGE_BY_ID.format(imageID))
        try:
            db.query(QUERY.DELETE_PRODUCT_IMAGE_BY_ID.format(imageID))

            UPLOAD_FOLDER = 'static/product_image'
            current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
           

            basedir = os.path.abspath(os.path.dirname(__file__))
            filePath = basedir + "/" + UPLOAD_FOLDER
            if not os.path.exists(filePath):
                os.makedirs(filePath)
         
            os.remove(os.path.join(basedir, UPLOAD_FOLDER, file['product_image']))
            images = db.query(QUERY.GET_PRODUCT_IMAGES_BY_ID.format(productID))
            if images:
                print(images)
                db.query(QUERY.UPDATE_PRODUCT_PRIMARY_IMAGE.format(images[0]['product_image_id'], productID))
            else:
                db.query(QUERY.UPDATE_PRODUCT_PRIMARY_IMAGE.format(0, productID))
               
            flash("Profile image deleted.", 'success')
        except Exception as e:
           
            flash(f"Error in deleting files: {e}", 'danger')
     
        return redirect(url_for('internal.product_detail', id = productID))
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')

@internal_bp.route('/inventory/product/get-subcategory', methods=['POST'])
@level_one_required
def get_subcategory():
    data = request.json
    selected_option = data.get('selected_option')
    datas = db.query(QUERY.GET_ALL_SUBCATS_FROM_CAT.format(selected_option))
    response_data = []
    for data in datas:
        response_data.append(data['subcategory_name'])
    return jsonify(response_data)

# Lv1 users view messages from all customers
@internal_bp.route('/get_messages_lv1', methods=['GET','POST'])
@level_one_required
def get_messages_lv1():

    query = QUERY.GET_ALL_MESSAGES_FROM_CUSTOMERS
    cus_messages = db.query(query)
    return render_template('messages/get_messages_lv1.html', cus_messages = cus_messages)

# Lv1 users reply messages to all customers
@internal_bp.route('/respond_messages_lv1/<int:message_id>', methods=['GET','POST'])
@level_one_required
def respond_messages_lv1(message_id):

    if request.method == 'POST':

        if 'message_content' in request.form:
            message_content = request.form['message_content']
        else:
            return "Missing message content", 400
        selected_message = db.queryOneResult(QUERY.GET_SELECTED_MESSAGE_FROM_CUSTOMER.format(message_id))
        user_id = selected_message.get("user_id")
        message_subject = selected_message.get("message_subject")
        message_timestamp = datetime.now()
        responder_id = session['user_id']

        try:
            db.query(QUERY.UPDATE_REPLIED_CUSTOMER_MESSAGE.format(message_id))
            new_message_id = db.querywithLastID(QUERY.INSERT_MESSAGES_TO_CUSTOMER.format(user_id, message_subject))

            db.querywithLastID(QUERY.INSERT_MESSAGES_CONTENTS_TO_CUSTOMER.format(new_message_id, message_content, message_timestamp, responder_id))
            flash('Your message is delivered to the customer!', 'success')
            query = QUERY.GET_ALL_MESSAGES_FROM_CUSTOMERS
            cus_messages = db.query(query)
            return render_template('messages/get_messages_lv1.html', cus_messages = cus_messages)
        except Exception as e:
            flash(f"Error in sending messages: {e}", 'danger')
    if request.method == 'GET':
            query = QUERY.GET_SELECTED_MESSAGE_FROM_CUSTOMER.format(message_id)
            cus_messages = db.query(query)
            return render_template('messages/respond_messages_lv1.html', cus_messages = cus_messages)
    

@internal_bp.route('/orderManagement', methods=['GET'])
@level_one_required
def orderManagement():

    orders = db.query(QUERY.GET_ALL_ORDERS)
    return render_template('order/order_management.html', orders = orders)

@internal_bp.route('/orderDetails/<int:id>', methods=['GET'])
@level_one_required
def orderDetails(id):
    shipping_prices = None
    order = db.queryOneResult(QUERY.GET_ORDERS_DETAILS_BY_ID.format(id))
    if order['order_status'] == 'placed':
        db.query(QUERY.UPDATE_ORDER_STATUS_BY_ID.format('preparing', session['user_id'], id))


    lines = db.query(QUERY.GET_PRODUCTS_BY_ORDER_ID.format(id))
    
    if order['order_status'] == 'pending':
        shipping_prices = db.query(QUERY.GET_ALL_SHIPPING_METHODS)
    payment =  db.queryOneResult(QUERY.GET_PAYMENT_BY_ORDER_ID.format( id)) 

    return render_template('order/order_detail.html', order = order, lines = lines, shipping_prices = shipping_prices, payment = payment)



@internal_bp.route('/order/<int:id>/<action>', methods=['GET'])
@level_one_required
def updateOrder(id, action):
    reason = request.args.get('reason')  # Get the 'reason' parameter from the request
    shipping_method_id = request.args.get('shipping') 
    
    order = db.queryOneResult(QUERY.GET_ORDERS_DETAILS_BY_ID.format(id))
    if not reason:
        reason = action
    

    if shipping_method_id:
        shipping_price = db.queryOneResult(QUERY.GET_SHIPPING_METHOD_BY_ID.format(shipping_method_id))
        db.query(QUERY.UPDATE_PENDING_ORDERS_WITH_SHIPPING.format(shipping_method_id, order['total_amount'] + Decimal(shipping_price['shipping_price']), id))
        reason = "Your shipping prices will be $" + str(shipping_price['shipping_price']) + ', please pay the order.'


    sendMessage(order['user_id'], 'Order ' + action, reason)

    # add point to customer
    if action == 'finished':
        updateCustomerPoints(order['total_amount'] -  Decimal(order['shipping_price']), order['user_id'])
        # check if bought any giftcard, and generate giftcard
        products =  db.query(QUERY.GET_PRODUCT_DETAILS_WITH_SUBCATEGORY_BY_ID.format(id))
        for p in products:
            if p['subcategory_id'] == 1:
                n = 0
                while n < p['quantity']:
                    number = re.search(r'\d+', p['product_name']).group(0)
                    generateGiftCard(number, 'buy', order['user_id'])
                    n += 1
    # reduce point for customer if cancel finished order
    elif action == 'cancelled' and order['order_status'] == 'finished':
        updateCustomerPoints(Decimal(order['shipping_price']) - order['total_amount'] , order['user_id'])
    

    if action == 'cancelled':
        payment =  db.queryOneResult(QUERY.GET_PAYMENT_BY_ORDER_ID.format( id))   
        if payment:
            db.queryOneResult(QUERY.UPDATE_PAYMENT_STATUS__TO_REFUND_BY_ORDER_ID.format( id))  


    db.query(QUERY.UPDATE_ORDER_STATUS_BY_ID.format(action, session['user_id'], id))

    return redirect(url_for('internal.orderManagement'))


@internal_bp.route('/inventory/<int:product_id>//setPrimaryImage', methods=['POST'])
@level_one_required
def setProductPrimaryImage(product_id):
    if request.method == 'POST':
        image_id = request.form.get('image_id')

        db.query(QUERY.UPDATE_PRODUCT_PRIMARY_IMAGE.format(image_id, product_id))
        flash('Primary Image Updated!', 'success')
     
        return redirect(url_for('internal.product_detail', id = product_id))
    else:
        flash("400 Bad request.", "danger")
        return redirect('/')



@internal_bp.route('/discounts/edit', methods=['GET','POST'])
@level_one_required
def editDiscount():
    id = 1
    categorySelected = 0
    subcategorySelected = 0

    promotion = db.queryOneResult(QUERY.GET_PROMOTION_DETAIL.format(id))
    products = db.query(QUERY.GET_PROMOTION_PRODUCTS.format(id))
    allCategories = db.query(QUERY.GET_ALL_CATEGORIES_EXCLUDES_GIFTCARD.format())
    allSubcategories = db.query(QUERY.GET_ALL_SUBCATEGORIES_EXCLUDES_GIFTCARD.format())

    if request.method == 'POST':
        categorySelected = request.form.get('categoryInput')
        subcategorySelected = request.form.get('subcategoryInput')
        if categorySelected != '':
            allSubcategories = db.query(QUERY.GET_ALL_SUBCATEGORIES_EXCLUDES_GIFTCARD_BY_ID.format(categorySelected))
            if len(allSubcategories) == 1:
                subcategorySelected = allSubcategories[0]['subcategory_id']
            for subcat in allSubcategories:
                allProducts = db.query(QUERY.GET_ALL_PRODUCTS_EXCLUDES_GIFTCARD_BY_SUBCAT_ID.format(subcat['subcategory_id']))
        if (subcategorySelected != "" and categorySelected != ''):
            allProducts = db.query(QUERY.GET_ALL_PRODUCTS_EXCLUDES_GIFTCARD_BY_SUBCAT_ID.format(subcategorySelected))
        elif (subcategorySelected != "" ):
            allProducts = db.query(QUERY.GET_ALL_PRODUCTS_EXCLUDES_GIFTCARD_BY_SUBCAT_ID.format(subcategorySelected))
        else:
            allProducts = db.query(QUERY.GET_ALL_PRODUCTS_EXCLUDES_GIFTCARD.format())
    else:
        allProducts = db.query(QUERY.GET_ALL_PRODUCTS_EXCLUDES_GIFTCARD.format())
    return render_template('inventory/edit_discount.html', promotion = promotion, products= products, allProducts = allProducts, allCategories = allCategories, allSubcategories = allSubcategories, subcategorySelected = subcategorySelected, categorySelected = categorySelected)

@internal_bp.route('/discounts/edit/submit', methods=['POST'])
@level_one_required
def editDiscountSubmit():

    data = request.json
    productId = data.get('product_id')
    checked = data.get('checked')
    
    if checked:
        db.query(QUERY.INSERT_DISCOUNT_PRODUCT.format(productId))
    else:
        db.query(QUERY.DELETE_DISCOUNT_PRODUCT.format(productId))
    return jsonify(checked)

@internal_bp.route('/discounts/edit/all', methods=['POST'])
@level_one_required
def editDiscountAll():
    id = 1 # discount id

    action = request.form.get('action')
    itemsChecked = request.form.getlist('itemsChecked')
    allItemsShown = request.form.getlist('allItemsShown')
    
    if action == "checkAll":
        query = 'INSERT INTO Promotion_Products (promotion_id, product_id) VALUES '
        for item in allItemsShown:
            if item not in itemsChecked:
                query += f'(1, "{item}"), '
        query = query[:-2] 
        query += ';'       
        flash('Discount added to products', 'success')

    elif action == "uncheckAll":
        items = ', '.join(allItemsShown)
        query = f'DELETE FROM Promotion_Products WHERE promotion_id = 1 AND product_id IN ({items});'
        flash('Products get back to normal price', 'success')

    db.query(query)

    return redirect(url_for('internal.editDiscount'))



# Lv1 users view account holder application messages from all customers
@internal_bp.route('/get_application_messages', methods=['GET','POST'])
@level_two_required
def get_application_messages():

    query = QUERY.GET_ALL_MESSAGES_FROM_CUSTOMERS
    cus_messages = db.query(query)
    return render_template('messages/get_application_messages.html', cus_messages = cus_messages)

# Lv1 users reply decision messages to all customers who applied for becoming account holder
@internal_bp.route('/respond_application_messages/<int:message_id>', methods=['GET','POST'])
@level_two_required
def respond_application_messages(message_id):

    if request.method == 'POST':

        if 'message_content' in request.form:
            message_content = request.form['message_content']
        else:
            return "Missing message content", 400
        selected_message = db.queryOneResult(QUERY.GET_SELECTED_MESSAGE_FROM_CUSTOMER.format(message_id))
        user_id = selected_message.get("user_id")
        message_subject = selected_message.get("message_subject")
        message_timestamp = datetime.now()
        responder_id = session['user_id']

        try:
            db.query(QUERY.UPDATE_REPLIED_CUSTOMER_MESSAGE.format(message_id))
            new_message_id = db.querywithLastID(QUERY.INSERT_MESSAGES_TO_CUSTOMER.format(user_id, message_subject))

            db.querywithLastID(QUERY.INSERT_MESSAGES_CONTENTS_TO_CUSTOMER.format(new_message_id, message_content, message_timestamp, responder_id))
            flash('You have declined this application!', 'warning')
            query = QUERY.GET_ALL_MESSAGES_FROM_CUSTOMERS
            cus_messages = db.query(query)
            return render_template('messages/get_application_messages.html', cus_messages = cus_messages)
        except Exception as e:
            flash(f"Error in sending messages: {e}", 'danger')
    if request.method == 'GET':
            query = QUERY.GET_SELECTED_MESSAGE_FROM_CUSTOMER.format(message_id)
            cus_messages = db.query(query)
            return render_template('messages/respond_application_messages.html', cus_messages = cus_messages)

# Lv1 users approve applications from all customers who applied for becoming account holder
@internal_bp.route('/approve_application_messages/<int:message_id>', methods=['GET','POST'])
@level_two_required
def approve_application_messages(message_id):

    if 'message_content' in request.form:
        message_content = request.form['message_content']
    else:
        return "Missing message content", 400
    selected_message = db.queryOneResult(QUERY.GET_SELECTED_MESSAGE_FROM_CUSTOMER.format(message_id))
    user_id = selected_message.get("user_id")
    message_subject = selected_message.get("message_subject")
    message_timestamp = datetime.now()
    responder_id = session['user_id']
    credit_limit_applied = float(db.queryOneResult(QUERY.SELECT_CREDIT_LIMIT_APPLIED.format(message_id))["monthly_limit"])

    try:
        db.query(QUERY.UPDATE_CUSTOMER_CREDIT_LIMIT.format(credit_limit_applied ,user_id))
        db.query(QUERY.UPDATE_REPLIED_CUSTOMER_MESSAGE.format(message_id))
        new_message_id = db.querywithLastID(QUERY.INSERT_MESSAGES_TO_CUSTOMER.format(user_id, message_subject))

        db.querywithLastID(QUERY.INSERT_MESSAGES_CONTENTS_TO_CUSTOMER.format(new_message_id, message_content, message_timestamp, responder_id))
        flash('You have approve this application!', 'success')
        query = QUERY.GET_ALL_MESSAGES_FROM_CUSTOMERS
        cus_messages = db.query(query)
        return render_template('messages/get_application_messages.html', cus_messages = cus_messages)
    except Exception as e:
        flash(f"Error in sending messages: {e}", 'danger')






@internal_bp.route('/order/customerPayWithCash/<int:id>', methods=['GET'])
@level_one_required
def customerPayWithCash(id):
   
    payment = db.queryOneResult(QUERY.GET_PAYMENT_BY_ORDER_ID.format(id))
    
    if not payment:
        order = db.queryOneResult(QUERY.GET_ORDERS_DETAILS_BY_ID.format(id))
        db.query(QUERY.INSERT_PAYMENT.format(order['user_id'], id, datetime.now(),order['total_amount'], 3  ))
        flash('Order paid with cash/eftpos.', 'success')
    elif payment['payment_type_id'] == 2:
        order = db.queryOneResult(QUERY.GET_ORDERS_DETAILS_BY_ID.format(id))
        db.query(QUERY.UPDATE_PAYMENT_STATUS_TO_CASH_PAYMENT_BY_ORDER_ID.format(datetime.now(), id ))
        flash('Order paid with cash/eftpos, account balance has been restored.', 'success')
    else:
        flash('Unauthorized', 'danger')

    return redirect(url_for('internal.orderDetails', id = id))

