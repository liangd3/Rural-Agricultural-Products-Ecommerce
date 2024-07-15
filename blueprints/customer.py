from datetime import datetime, date
from flask import Blueprint, flash,render_template,request,redirect, session,url_for, jsonify
from util.util import customer_required, updatePromotionStatus, get_price_after_discount, sendMessage, generateGiftCard, verifyProductInPromotion
import db.queryStrings as QUERY
import db.db as db
from decimal import Decimal


customer_bp = Blueprint('customer',__name__,template_folder='templates')


# Customer Dashboard
@customer_bp.route('/customer')
@customer_required
def customer_dashboard():
    print('{timestamp} -- customer dashboard request started'.format(timestamp=datetime.utcnow().isoformat()))
    query = QUERY.FIND_A_USER_BY_EMAIL.format(session['email'])
    customer_dict = db.queryOneResult(query)
    customer = list(customer_dict.values())

    updatePromotionStatus()
    
    promotions = db.query(QUERY.GET_PROMOTION_LIST)
    categories = db.query(QUERY.GET_ALL_CATEGORIES)
    subcategories = db.query(QUERY.GET_ALL_SUBCATEGORIES)
    # products = db.query(QUERY.GET_ALL_PRODUCTS)
    # hot_products = db.query(QUERY.GET_HOT_PRODUCTS)
    hot_products = db.query(QUERY.GET_HOT_PRODUCTS)

    # products_images = db.query(QUERY.GET_ALL_PRODUCTS_IMAGES)
    news = db.query(QUERY.GET_ALL_NEWS)
    user_id = session['user_id']
    query = QUERY.GET_ALL_MESSAGES_FROM_LV1.format(user_id)
    cus_messages = db.query(query)
    session['cus_messages'] = cus_messages

    # for i, product in enumerate(products):
    #     discountedPrice = get_price_after_discount(product['product_id'], product['product_price'])
    #     if discountedPrice: 
    #         products[i]['discounted_price'] = discountedPrice
    #     if product['stock_quantity'] >= 80:
    #         hot_products.append(product)
    # for i, product in enumerate(hot_products):
    #     discountedPrice = get_price_after_discount(product['product_id'], product['product_price'])
    #     if discountedPrice: 
    #         hot_products[i]['discounted_price'] = discountedPrice
    print('{timestamp} -- customer dashboard request ended'.format(timestamp=datetime.utcnow().isoformat()))
    return render_template('customer/customer_dashboard.html', hot_products=hot_products,  promotions=promotions, customer=customer, news=news, cus_messages=cus_messages, categories = categories, subcategories = subcategories )

@customer_bp.route('/products', methods = ['GET', 'POST'])

def all_products():
    print('{timestamp} -- customer products page request started'.format(timestamp=datetime.utcnow().isoformat()))
    nav_bar_redirect = True
    updatePromotionStatus()
    if request.method == 'POST':
        search_subcategory = request.form.get('search_subcategory')
        
        search = request.form.get('search')
        searchterm = f"%{search}%"
        if not search_subcategory:
            products = db.query(QUERY.SEARCH_ALL_PRODUCTS_WITH_NAME.format(searchterm))
        else:
            products = db.query(QUERY.SEARCH_ALL_PRODUCTS_WITH_NAME_AND_SUBCATEGORY_ID.format(search_subcategory, searchterm))
    else:
        subcategoryID = request.args.get('subcategory')  
        if subcategoryID:
            products = db.query(QUERY.GET_ALL_PRODUCTS_WITH_SUBCATEGORY_ID.format(subcategoryID))        
        else:
            products = db.query(QUERY.GET_ALL_PRODUCTS)
            nav_bar_redirect = False
    
    categories = db.query(QUERY.GET_ALL_CATEGORIES)
    subcategories = db.query(QUERY.GET_ALL_SUBCATEGORIES)
    
    subcategories_in_promotion = db.query(QUERY.GET_ALL_PROMOTION_SUBCATOGERIES_TO_VERIFY)  
    products_in_promotion = db.query(QUERY.GET_ALL_PROMOTION_PRODUCTS_TO_VERIFY)  
    categories_in_promotion = db.query(QUERY.GET_ALL_PROMOTION_CATOGERIES_TO_VERIFY) 

    for i, product in enumerate(products):
        if verifyProductInPromotion(subcategories_in_promotion, products_in_promotion, categories_in_promotion, product['product_id'], product['subcategory_id']):
            discountedPrice = get_price_after_discount(product['product_id'], product['product_price'], 2)
            if discountedPrice: 
                products[i]['discounted_price'] = discountedPrice
    print('{timestamp} -- customer products page request ended'.format(timestamp=datetime.utcnow().isoformat()))
    return render_template('customer/products.html',products=products, subcategories=subcategories, categories=categories, nav_bar_redirect = nav_bar_redirect )


# Customer Profile
@customer_bp.route('/customer/profile')
@customer_required
def customer_profile():
    query = QUERY.GET_CUSTOMER_PROFILE.format(session['user_id'])
    profile = db.queryOneResult(query)
    cus_messages = session.get('cus_messages', [])


    addresses = db.query(QUERY.GET_USER_ADDRESSES.format(session['user_id']))
    return render_template('customer/customer_profile.html', profile = profile, addresses = addresses, cus_messages=cus_messages)


@customer_bp.route('/customer/profile/edit', methods = ['GET', 'POST'])
@customer_required
def customer_profile_edit():
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
        db.query(QUERY.EDIT_CUSTOMER_PROFILE.format(firstName, lastName, phone ,session['user_id']))
        query = QUERY.GET_CUSTOMER_PROFILE.format(session['user_id'])
        profile = db.queryOneResult(query)
        session['first_name'] = firstName
        session['last_name'] = lastName
        flash('Profile updated sucssesfully.', 'success')
    return render_template('customer/customer_profile.html', profile = profile)

# Customer Monthly Payment
@customer_bp.route('/customer/account_holder')
@customer_required
def customer_account_holder():
    query = QUERY.FIND_A_USER_BY_EMAIL.format(session['email'])
    customer_dict = db.queryOneResult(query)
    customer = list(customer_dict.values())
    cus_messages = session.get('cus_messages', [])

    return render_template('customer/account_holder.html',customer=customer, cus_messages=cus_messages)

# Customer Monthly Payment
@customer_bp.route('/customer/submit_account_holder_application', methods=['POST'])
@customer_required
def submit_account_holder_application():

    monthly_limit = request.form['monthlyLimit']
    user_id = session['user_id']

# Account Information
    legal_entity = request.form.getlist('legalEntity')
    other_entity_details = request.form.get('otherEntityDetails', '').replace("'", "''")
    if 'Other' in legal_entity and other_entity_details:
        legal_entity.remove('Other')
        legal_entity.append(f'Other: {other_entity_details}')
    legal_entity_str = ', '.join(legal_entity)
    
    account_name = request.form.get('accountName', '').replace("'", "''")
    trading_name = request.form.get('tradingName', '').replace("'", "''")
    company_number = request.form.get('companyNumber', '').replace("'", "''")
    gst_number = request.form.get('gstNumber', '').replace("'", "''")
    
    # Postal Address
    postal_number = request.form.get('postalNumber', '').replace("'", "''")
    postal_street = request.form.get('postalStreet', '').replace("'", "''")
    postal_suburb = request.form.get('postalSuburb', '').replace("'", "''")
    postal_city = request.form.get('postalCity', '').replace("'", "''")
    postal_province = request.form.get('postalProvince', '').replace("'", "''")
    postal_postcode = request.form.get('postalPostcode', '').replace("'", "''")
    
    # Residential Address
    residential_number = request.form.get('residentialNumber', '').replace("'", "''")
    residential_street = request.form.get('residentialStreet', '').replace("'", "''")
    residential_suburb = request.form.get('residentialSuburb', '').replace("'", "''")
    residential_city = request.form.get('residentialCity', '').replace("'", "''")
    residential_province = request.form.get('residentialProvince', '').replace("'", "''")
    residential_postcode = request.form.get('residentialPostcode', '').replace("'", "''")
    
    # Delivery Address
    delivery_number = request.form.get('deliveryNumber', '').replace("'", "''")
    delivery_street = request.form.get('deliveryStreet', '').replace("'", "''")
    delivery_suburb = request.form.get('deliverySuburb', '').replace("'", "''")
    delivery_city = request.form.get('deliveryCity', '').replace("'", "''")
    delivery_province = request.form.get('deliveryProvince', '').replace("'", "''")
    delivery_postcode = request.form.get('deliveryPostcode', '').replace("'", "''")
    
    # Primary Contact Information
    primary_contact_name = request.form.get('primaryContactName', '').replace("'", "''")
    primary_contact_relationship = request.form.get('primaryContactRelationship', '').replace("'", "''")
    primary_contact_dob = request.form.get('primaryContactDOB', '').replace("'", "''")
    primary_contact_postal_address = request.form.get('primaryContactPostalAddress', '').replace("'", "''")
    primary_contact_home_phone = request.form.get('primaryContactHomePhone', '').replace("'", "''")
    primary_contact_mobile = request.form.get('primaryContactMobile', '').replace("'", "''")
    primary_contact_email = request.form.get('primaryContactEmail', '').replace("'", "''")
    primary_contact_id = request.form.get('primaryContactID', '').replace("'", "''")
    primary_contact_signature = request.form.get('primaryContactSignature', '').replace("'", "''")
    
    # Additional Contact Information
    additional_contact_name = request.form.get('additionalContactName', '').replace("'", "''")
    additional_contact_relationship = request.form.get('additionalContactRelationship', '').replace("'", "''")
    additional_contact_dob = request.form.get('additionalContactDOB', '').replace("'", "''")
    additional_contact_postal_address = request.form.get('additionalContactPostalAddress', '').replace("'", "''")
    additional_contact_home_phone = request.form.get('additionalContactHomePhone', '').replace("'", "''")
    additional_contact_mobile = request.form.get('additionalContactMobile', '').replace("'", "''")
    additional_contact_email = request.form.get('additionalContactEmail', '').replace("'", "''")
    additional_contact_id = request.form.get('additionalContactID', '').replace("'", "''")
    additional_contact_signature = request.form.get('additionalContactSignature', '').replace("'", "''")
    
    message_content = f"""
    Account Information:
    Legal Entity: {legal_entity_str},
    Account Name: {account_name},
    Trading Name: {trading_name},
    Company Number: {company_number},
    GST Number: {gst_number},
    
    Postal Address:
    Number: {postal_number},
    Street Name: {postal_street},
    Suburb: {postal_suburb},
    City: {postal_city},
    Province: {postal_province},
    Postcode: {postal_postcode},
    
    Residential Address:
    Number: {residential_number},
    Street Name: {residential_street},
    Suburb: {residential_suburb},
    City: {residential_city},
    Province: {residential_province},
    Postcode: {residential_postcode},
        
    Delivery Address:
    Number: {delivery_number},
    Street Name: {delivery_street},
    Suburb: {delivery_suburb},
    City: {delivery_city},
    Province: {delivery_province},
    Postcode: {delivery_postcode},
    
    Primary Contact Information:
    Full Name: {primary_contact_name},
    Relationship to Account: {primary_contact_relationship},
    Date of Birth: {primary_contact_dob},
    Postal Address: {primary_contact_postal_address},
    Home Phone: {primary_contact_home_phone},
    Mobile: {primary_contact_mobile},
    Email: {primary_contact_email},
    Driver''s Licence/Passport No.: {primary_contact_id},
    Signature: {primary_contact_signature},
    
    Additional Contact Information:
    Full Name: {additional_contact_name},
    Relationship to Account: {additional_contact_relationship},
    Date of Birth: {additional_contact_dob},
    Postal Address: {additional_contact_postal_address},
    Home Phone: {additional_contact_home_phone},
    Mobile: {additional_contact_mobile},
    Email: {additional_contact_email},
    Driver''s Licence/Passport No.: {additional_contact_id},
    Signature: {additional_contact_signature},
    Monthly Limit applied: {monthly_limit}
    """
    create_new_message = QUERY.SET_ACCOUNT_HOLDER_APPLICATION_TO_MESSAGE.format(user_id, 'Account Holder Application')
    message_id = db.querywithLastID(create_new_message)

    create_new_message_content = QUERY.SET_ACCOUNT_HOLDER_APPLICATION_TO_MESSAGE_CONTENT.format(message_id, message_content, datetime.now())

    db.query(create_new_message_content)
    flash('Application submitted successfully!', 'success')
    return redirect(url_for('customer.customer_dashboard'))



# Customer View Products
@customer_bp.route('/product/<int:id>')

def customer_products(id):
    updatePromotionStatus()
    product = db.queryOneResult(QUERY.GET_PRODUCT_DATAILS_BY_ID.format(id))
    products_images = db.query(QUERY.GET_PRODUCT_IMAGES_BY_ID.format(id))
    reviews = db.query(QUERY.GET_PRODUCT_REVIEWS_BY_ID.format(id))
    print(product)
    applied_promotions = []
    discountedPrice = get_price_after_discount(product['product_id'], product['product_price'], 2)
    if discountedPrice:
        subcategories_in_promotion = db.query(QUERY.GET_ALL_PROMOTION_SUBCATOGERIES_TO_VERIFY)  
        for s in subcategories_in_promotion:
            if s['subcategory_id'] == product['subcategory_id']:
                applied_promotions.append(s)
        products_in_promotion = db.query(QUERY.GET_ALL_PROMOTION_PRODUCTS_TO_VERIFY)  
        for p in products_in_promotion:
            if p['product_id'] == product['product_id']:
                applied_promotions.append(p)

        categories_in_promotion = db.query(QUERY.GET_ALL_PROMOTION_CATOGERIES_TO_VERIFY) 
        for c in categories_in_promotion:
            if c['subcategory_id'] == product['subcategory_id']:
                applied_promotions.append(c)


    
    canleavereview = False
    if session and session['user_id']:
        cus_messages = session.get('cus_messages', [])
    else:
        cus_messages = None
    if session and session['user_id']:
        bought =  db.query(QUERY.CHECK_PRODUCT_BOUGHT_BY_CUSTOMER_ID.format(session['user_id'], id))
        if bought:
            canleavereview = True
            reviewed = db.query(QUERY.CHECK_REVIEW_LEFT_BY_CUSTOMER_ID.format(session['user_id'], id))
            if reviewed:
                canleavereview = False
    
    return render_template('customer/product_details.html', products_images=products_images, product=product, reviews = reviews, discountedPrice = discountedPrice, canleavereview = canleavereview, cus_messages=cus_messages, applied_promotions = applied_promotions)



@customer_bp.route('/customer/product/add', methods = ['POST'])
@customer_required
def add_product():
    updatePromotionStatus()

    data = request.json
    product_id = data.get('product_id')
    qty = int(data.get('qty'))
    user_id = session['user_id']

    product = db.queryOneResult(QUERY.GET_PRODUCT_DETAIL.format(product_id))
    # Check stock
    if product['stock_quantity'] < qty:
        response = 'Item out of stock.'
    else:
        current_qty = db.queryOneResult(QUERY.CHECK_CART_QTY.format(session['user_id'], product_id))
        if current_qty:
            target_qty = int(current_qty['qty']) + qty
            if target_qty < 0:
                db.query(QUERY.DELETE_PRODUCT_FROM_CART.format(user_id, product_id))
            else:
                db.query(QUERY.PLUS_SOME_TO_CART.format(target_qty, user_id, product_id))
        else:
            target_qty = qty
            db.query(QUERY.INSERT_TO_CART.format(user_id, product_id, qty))
        response = target_qty
    return jsonify(response)

@customer_bp.route('/customer/cart/product/update', methods = ['POST'])
@customer_required
def update_product_qty():
    updatePromotionStatus()

    data = request.json
    product_id = data.get('product_id')
    qty = abs(int(data.get('qty')))

    if qty == 0:
        db.query(QUERY.DELETE_PRODUCT_FROM_CART.format(session['user_id'], product_id))
        return redirect(url_for('customer.cart'))
    else:
        db.query(QUERY.PLUS_SOME_TO_CART.format(qty, session['user_id'], product_id))
        response = qty
        return jsonify(response)

@customer_bp.route('/customer/shopping_cart/totalQty', methods = ['POST'])
@customer_required
def getShoppingCartTotalQty():
    return jsonify(db.queryOneResult(QUERY.GET_SHOPPING_CART_TOTAL_QTY.format(session['user_id'])).get('total'))


@customer_bp.route('/customer/cart/<int:pid>/delete')
@customer_required
def cart_delete(pid):
    db.query(QUERY.DELETE_PRODUCT_FROM_CART.format(session['user_id'], pid))
    flash('Item deleted.', 'warning')
    return redirect(url_for('customer.cart'))


# Customer Shopping Cart
@customer_bp.route('/customer/cart', methods = ['GET','POST'])
@customer_required
def cart():
    cus_messages = session.get('cus_messages', [])

    updatePromotionStatus()
    mustPickup = False

    products = db.query(QUERY.GET_SHOPPING_CART.format(session['user_id']))
    for key, product in enumerate(products):
        discountedPrice = get_price_after_discount(product['product_id'], product['product_price'], product['qty'])
        if discountedPrice and type(discountedPrice) != str: 
            products[key]['discounted_price'] = discountedPrice
        elif discountedPrice == 'buyOneGetOneFree':
            products[key]['discounted_price'] = 'Buy One Get One Free'
            products[key]['bogof_price'] = product['product_price'] * ((product['qty'] // 2) + (product['qty'] % 2))

        # Check stock availability again, if not back to cart
        if product['stock_quantity'] < product['qty']:
            product['qty'] = product['stock_quantity']
            flash('warning', f'Not enough stock for {product["product_name"]}. Maximum quantity applied.')
        # Check if stock must be picked up
        if product['oversized'] == 2:
            mustPickup = True


    if request.method == 'POST':
        return jsonify(products)
    else:
        return render_template('customer/cart.html', products = products, mustPickup = mustPickup, cus_messages=cus_messages)
    

def calculateTotal(uid, pickup):
    calculation = {}
    calculation['totalExShipping'] = 0

    shippingMethod = db.query(QUERY.GET_ALL_SHIPPING.format())
    products = db.query(QUERY.GET_SHOPPING_CART.format(uid))
    customer = db.queryOneResult(QUERY.GET_CUSTOMER_DETAIL.format(uid))
    creditUsed = db.queryOneResult(QUERY.GET_CREDIT_USED_BY_USER.format(uid)).get('credit_used')

    calculation['shipping'] = shippingMethod[0]['shipping_price']

    for product in products:
        # calculate price
        discount = get_price_after_discount(product['product_id'], product['product_price'], product['qty'])
        if discount: 
            if discount == "buyOneGetOneFree":
                calculation['totalExShipping'] += product['product_price'] * ((product['qty'] // 2) + (product['qty'] % 2))
            else:
                calculation['totalExShipping'] += discount * product['qty']
        else:
            calculation['totalExShipping'] += product['product_price'] * product['qty']

        # Calculate shipping
        if product['oversized'] == 1:
            calculation['shipping'] = shippingMethod[1]['shipping_price']
            calculation['oversized'] = True
        if product['oversized'] == 2:
            calculation['mustPickup'] = True
        else:
            calculation['oversized'] = False
            calculation['mustPickup'] = False
    if pickup:
        calculation['shipping'] = shippingMethod[2]['shipping_price']
    
    calculation['gst'] = round(float(calculation['totalExShipping']) * float(1-(1/1.15)), 2)
    calculation['totalExShippingExGst'] = float(calculation['totalExShipping']) - float(calculation['gst'])
    calculation['total'] = float(calculation['totalExShipping']) + calculation['shipping']
    calculation['remainingLimit'] = customer['credit_limit'] - (creditUsed or 0)  # Get remaining credit limit
    return calculation

# Customer Checkout
@customer_bp.route('/customer/checkout', methods=['GET', 'POST'])
@customer_required
def checkout():

    cus_messages = session.get('cus_messages', [])

    updatePromotionStatus()

    if request.method == 'POST':
        products = db.query(QUERY.GET_SHOPPING_CART.format(session['user_id']))
    
        if products:    #check if anything in shopping cart 
            if any(product['oversized'] == 2 for product in products):
                pickup = True 
            else:
                pickup = request.form.get('pickup')

            calculation = calculateTotal(session['user_id'], pickup)

            addresses = db.query(QUERY.GET_USER_ADDRESSES.format(session['user_id']))
            for key, address in enumerate(addresses):
                addresses[key]['full_address'] = (f'{address["unit_number"]}, ' if address["unit_number"] else "") + f'{address["address_line1"]}, ' + (f'{address["address_line2"]},' if address["address_line2"] else "") + f'{address["city"]}, {address["region"]} {address["postcode"]}'

            
            customer = db.queryOneResult(QUERY.GET_CUSTOMER_DETAIL.format(session['user_id']))

            giftcards = db.query(QUERY.GET__FIVE_GIFTCARDS_WITH_HIGHEST_BALANCE_BY_ID.format(session['user_id']))
            return render_template('customer/checkout.html', calculation = calculation, addresses = addresses, customer = customer, pickup = pickup, giftcards = giftcards , cus_messages=cus_messages)

        else: flash('Shopping cart is empty.', 'warning')
    return redirect(url_for('customer.cart')) 

def addressCombiner(unit, address1, address2, city, region, postcode):
    unitIf = f'{unit}, ' if unit else ''
    add2If = f'{address2}, ' if address2 else ''
    return f'{unitIf} {address1}, {add2If} {city}, {region} {postcode}'

# Customer Payment
@customer_bp.route('/customer/cart/<action>', methods=['GET', 'POST'])
@customer_required
def payment(action):
    totalExShipping = 0

    if request.method == 'POST':
        unit = request.form.get('unit') 
        unit = unit if unit else ''
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        address2 = address2 if address2 else ''
        postcode = request.form.get('postcode') 
        city = request.form.get('city') 
        region = request.form.get('region') 
        address = addressCombiner(unit, address1, address2, city, region, postcode)
        saveAddress = request.form.get('saveThisAddress')

        pickup = request.form.get('pickup')
        paymentMethod = request.form.get('payment-method')
   

        checkout_calculated_total = request.form.get('calculated_total')

        products = db.query(QUERY.GET_SHOPPING_CART.format(session['user_id']))
        
        # Get payment type
        if not paymentMethod:
            paymentMethodInId = 1
        else:

        
            paymentMethodInId = db.queryOneResult(QUERY.GET_PAYMENT_TYPE_ID.format(f'%{paymentMethod}%')).get('payment_type_id')

        #calculate totals
        calculation = calculateTotal(session['user_id'], pickup)

        # Check stock availability again, if not back to cart
        for product in products:
            if product['stock_quantity'] < product['qty']:
                flash('Some of the items are out of stock. Please try again.', 'warning')
                return redirect(url_for('customer.cart'))
            
        # check sale price
        calculatedTotal = float(calculation['totalExShipping']) if pickup or calculation['mustPickup'] else float(calculation['total'])
        if float(checkout_calculated_total) != calculatedTotal:
            #print(f'{pickup} {calculation["mustPickup"]} checkout_calculated_total: {checkout_calculated_total}; calculatedTotal: {calculatedTotal}')
            flash('Some of the price of the item has changed. Please confirm and proceed to checkout again.', 'warning')
            return redirect(url_for('customer.cart'))

        # check remaining credit
        if calculation['remainingLimit'] < calculation['total'] and paymentMethod == "account":
            flash('Not enough credit. Please use the other payment methods.', 'warning')
            return redirect(url_for('customer.checkout'))
        
     
        
        paymentAmount = calculation['total']

        
        # sort shipping method ID
        if pickup or calculation['mustPickup']:
            shippingMethodId = 3
        elif calculation['oversized']:
            shippingMethodId = 2
        elif not calculation['oversized']:
            shippingMethodId = 1
        if action == "request_quote":
            shippingMethodId = None
        
        # new order
        orderID = db.querywithLastID(QUERY.INSERT_NEW_ORDER.format(session['user_id'], date.today(), calculation['total'], shippingMethodId, address))

        for product in products:
        # take stock away
            newStockLevel = product['stock_quantity'] - product['qty']
            db.query(QUERY.UPDATE_PRODUCT_QUANTITY_BY_ID.format(newStockLevel, product['product_id']))
         # add order details
            discountedPrice = get_price_after_discount(product['product_id'], product['product_price'], product['qty'])
            if discountedPrice: 
                if discountedPrice == "buyOneGetOneFree":
                    calculation['totalExShipping'] += product['product_price'] * ((product['qty'] // 2) + (product['qty'] % 2))
                else:
                    calculation['totalExShipping'] += discountedPrice * product['qty']
            else:
                calculation['totalExShipping'] += product['product_price'] * product['qty']
            if discountedPrice and type(discountedPrice) != str:
                finalPrice = discountedPrice
                discountRate = 1 - round( discountedPrice/ product['product_price'], 2)
            else:
                finalPrice = product['product_price']
                discountRate = 0
            db.query(QUERY.INSERT_ORDER_DETAIL.format(orderID, product['product_id'], product['product_name'], product['qty'], product['product_price'], discountRate,finalPrice))

        # add payment detail
      
        payment_id = db.querywithLastID(QUERY.INSERT_PAYMENT.format(session['user_id'], orderID, datetime.now(), paymentAmount, paymentMethodInId))
     
        # deduct gift card
        remaning_balance = Decimal(paymentAmount)
        selected_giftcards = request.form.getlist('selected_giftcards')
        for i in selected_giftcards:
            card = db.queryOneResult(QUERY.GET_GIFTCARD_BY_CARD_ID.format(i))
            if card['user_id'] != session['user_id']:
                flash('Unaothorized!', 'danger')
                return redirect(url_for('customer.customer_orders'))
            if remaning_balance > card['gift_card_amount']:
                remaning_balance = remaning_balance - card['gift_card_amount']
                db.query(QUERY.UPDATE_GIFT_CARD_AMOUNT_BY_ID.format(0, i))
                db.query(QUERY.INSERT_GIFT_CARD_HISTORY.format(payment_id, i, card['gift_card_amount']))
            else:
                
                db.query(QUERY.UPDATE_GIFT_CARD_AMOUNT_BY_ID.format(card['gift_card_amount'] - remaning_balance , i))
                db.query(QUERY.INSERT_GIFT_CARD_HISTORY.format(payment_id, i, remaning_balance))
                remaning_balance = 0
                break
        

        if paymentAmount != remaning_balance:
             db.query(QUERY.UPDATE_PAYMENT_WITH_GIFT_CARD.format(remaning_balance, orderID ))


        # save address
        if saveAddress and not pickup:
            db.query(QUERY.INSERT_NEW_ADDRESS.format(session['user_id'], unit, address1, address2, city, region, postcode))

        # send a message to staff/manager:
        if action == "request_quote":
            # message content
            print("message content")
            pass

        # clear cart
        db.query(QUERY.DELETE_ALL_ITEM_IN_CART.format(session['user_id']))

        cus_messages = session.get('cus_messages', [])
        return render_template('customer/checkout_success.html',cus_messages=cus_messages)
        
    return redirect(url_for('customer.cart')) 

# Return an address
@customer_bp.route('/get_address', methods=['POST'])
@customer_required
def get_address():
    data = request.json
    address_id = data.get('address_id')
    return jsonify(db.queryOneResult(QUERY.GET_ADDRESS_BY_ID.format(address_id)))

# Applying a coupon
@customer_bp.route('/apply_coupon', methods=['POST'])
@customer_required
def apply_coupon():
    coupon_code = request.json.get('coupon_code')
    return jsonify(db.queryOneResult(QUERY.GET_COUPON.format(coupon_code)))


# add new address
@customer_bp.route('/edit_address', methods=['POST'])
@customer_required
def edit_address():
    address_id = int(request.form.get('editaddress_id'))
    addresses = db.query(QUERY.GET_USER_ADDRESSES.format(session['user_id']))
    
    for i in addresses:
        if i['address_id'] == address_id:
            return render_template('customer/address_detail.html' , address = i)

    flash('Unaothorized!', 'danger')
    return redirect(url_for('customer.customer_profile'))
    

# Update address
@customer_bp.route('/edit_address_form', methods=['POST'])
@customer_required
def edit_address_form():


    addresses = db.query(QUERY.GET_USER_ADDRESSES.format(session['user_id']))
    unitNumber = request.form.get('unit_number')
    address_line1 = request.form.get('address_line_1')
    address_line2 = request.form.get('address_line_2')
    region = request.form.get('region')
    city = request.form.get('city')
    postcode = request.form.get('postcode')
    address_id = int(request.form.get('address_id'))

    
    for i in addresses:

        if i['address_id'] == address_id:
           
            db.query(QUERY.UPDATE_ADDRESS_BY_ID.format(unitNumber, address_line1, address_line2,region,city, postcode, address_id  ))


            flash('Address updated', 'success')
            return redirect(url_for('customer.customer_profile'))

    flash('Unaothorized!', 'danger')
    return redirect(url_for('customer.customer_profile'))

# add new address
@customer_bp.route('/add_new_address', methods=['POST'])
@customer_required
def add_new_address():

    return render_template('customer/address_detail.html' )

# add new address
@customer_bp.route('/add_new_address_form', methods=['POST'])
@customer_required
def add_new_address_form():


    unitNumber = request.form.get('unit_number')
    address_line1 = request.form.get('address_line_1')
    address_line2 = request.form.get('address_line_2')
    region = request.form.get('region')
    city = request.form.get('city')
    postcode = request.form.get('postcode')


    db.query(QUERY.ADD_NEW_ADDRESS.format(unitNumber, address_line1, address_line2,region,city, postcode, session['user_id'] ))


    flash('New address added', 'success')
    return redirect(url_for('customer.customer_profile'))

# Delete address
@customer_bp.route('/delete_address', methods=['POST'])
@customer_required
def delete_address():

    address_id = int(request.form.get('deleteaddress_id'))
    addresses = db.query(QUERY.GET_USER_ADDRESSES.format(session['user_id']))

  
    for i in addresses:
       
        if i['address_id'] == address_id:
            print('TRUE')
        
            db.query(QUERY.DELETE_ADDRESS_BY_ID.format(address_id  ))
            if len(addresses) > 1:
                for i in addresses:
                    if i['address_id'] != address_id:
                        address_id = i['address_id']
                        db.query(QUERY.SET_PRIMARY_ADDRESS_BY_ID.format(address_id,session['user_id']   ))
                        break
                
            flash('Address deleted', 'success')
            return redirect(url_for('customer.customer_profile'))

    flash('Unaothorized!', 'danger')
    return redirect(url_for('customer.customer_profile'))


@customer_bp.route('/set_primary_address', methods=['POST'])
@customer_required
def set_primary_address():

    address_id = int(request.form.get('primaryaddress_id'))
    addresses = db.query(QUERY.GET_USER_ADDRESSES.format(session['user_id']))
 
    for i in addresses:
        if i['address_id'] == address_id:

            db.query(QUERY.SET_PRIMARY_ADDRESS_BY_ID.format(address_id,session['user_id']   ))
            flash('Primary address updated!', 'success')
            return redirect(url_for('customer.customer_profile'))

    flash('Unaothorized!', 'danger')
    return redirect(url_for('customer.customer_profile'))


# Customer Orders and Payments
@customer_bp.route('/customer/orders', methods=['GET'])
@customer_required
def customer_orders():
    cus_messages = session.get('cus_messages', [])

    user_id = session['user_id']
    orders = db.query(QUERY.GET_CUSTOMER_ORDERS_WITH_PAYMENTS_AND_SHIPPING.format(user_id))

    return render_template('customer/orders.html', orders=orders)

# Customer Orders details
@customer_bp.route('/customer/orders/<int:id>', methods=['GET'])
@customer_required
def customer_order_details(id):

    order = db.queryOneResult(QUERY.GET_ORDERS_DETAILS_BY_ID.format(id))

    if not order or order['user_id'] != session['user_id']:
        flash('Unaothorized!', 'danger')
        return redirect(url_for('customer.customer_orders'))

    lines = db.query(QUERY.GET_PRODUCTS_BY_ORDER_ID.format(id))
    

    payment =  db.queryOneResult(QUERY.GET_PAYMENT_BY_ORDER_ID.format( id)) 

    return render_template('customer/order_detail.html', order = order, lines = lines,  payment = payment)

# Customer pay order
@customer_bp.route('/customer/orders/pay/<int:id>', methods=['GET','POST'])
@customer_required
def customer_pay_order(id):
    order = db.queryOneResult(QUERY.GET_ORDERS_DETAILS_BY_ID.format(id))
    if not order or order['user_id'] != session['user_id']:
        flash('Unaothorized!', 'danger')
        return redirect(url_for('customer.customer_orders'))
    

    if request.method == 'POST':
        payment =  db.queryOneResult(QUERY.GET_PAYMENTS_BY_ORDER_ID.format(id))
        print(payment)
        if not payment:   
            payment_id = db.querywithLastID(QUERY.INSERT_PAYMENT.format(session['user_id'],id,  datetime.now(),order['total_amount'], 1 ))
        else:
            payment_id = payment['payment_id']
            db.query(QUERY.UPDATE_PAYMENT_STATUS_TO_CARD_PAYMENT_BY_ORDER_ID.format(datetime.now(), id))

        remaning_balance = order['total_amount']
        selected_giftcards = request.form.getlist('selected_giftcards')
        for i in selected_giftcards:
            card = db.queryOneResult(QUERY.GET_GIFTCARD_BY_CARD_ID.format(i))
            if card['user_id'] != session['user_id']:
                flash('Unaothorized!', 'danger')
                return redirect(url_for('customer.customer_orders'))
            if remaning_balance > card['gift_card_amount']:
                remaning_balance = remaning_balance - card['gift_card_amount']
                db.query(QUERY.UPDATE_GIFT_CARD_AMOUNT_BY_ID.format(0, i))
                db.query(QUERY.INSERT_GIFT_CARD_HISTORY.format(payment_id, i, card['gift_card_amount']))
            else:
                
                db.query(QUERY.UPDATE_GIFT_CARD_AMOUNT_BY_ID.format(card['gift_card_amount'] - remaning_balance , i))
                db.query(QUERY.INSERT_GIFT_CARD_HISTORY.format(payment_id, i, remaning_balance))
                remaning_balance = 0
                break
        

        if order['total_amount'] != remaning_balance:
             db.query(QUERY.UPDATE_PAYMENT_WITH_GIFT_CARD.format(remaning_balance, id))
        
        # # Validate gift card if any
        # if couponCode:
        #     giftCard = db.queryOneResult(QUERY.GET_GIFT_CARD_DETAIL.format(couponCode))
        #     if giftCard:
        #         if couponAmount > giftCard['gift_card_amount']:
        #             flash('The gift card doesn\' have enough balance.', 'warning')
        #             return redirect(url_for('customer.checkout'))
        #         giftCardId = giftCard['gift_card_id']
        # else: giftCard = {}
        # couponAmount = couponAmount if couponAmount else 0
        # paymentAmount = total_amount - couponAmount


 
        # if giftCard: 
        #     db.query(QUERY.UPDATE_PAYMENT_WITH_GIFTCARD_BY_ORDER_ID.format(paymentAmount -couponAmount, giftCardId, couponAmount, id))
        #     newGiftCardAmount = giftCard['gift_card_amount'] - couponAmount
        #     db.query(QUERY.UPDATE_GIFT_CARD_AMOUNT.format(newGiftCardAmount, couponCode))
           

        flash('Payment success!', 'success')
        return redirect(url_for('customer.customer_orders'))

    
    
    giftcards = db.query(QUERY.GET__FIVE_GIFTCARDS_WITH_HIGHEST_BALANCE_BY_ID.format(session['user_id']))
    return render_template('customer/order_payment.html', order = order, giftcards = giftcards) 


# Customer view all response messages from the lv1 users
@customer_bp.route('/customer/get_messages', methods=['GET','POST'])
@customer_required
def get_messages():

    user_id = session['user_id']
    query = QUERY.GET_ALL_MESSAGES_FROM_LV1.format(user_id)
    cus_messages = db.query(query)
    return render_template('messages/get_messages.html', cus_messages = cus_messages)


@customer_bp.route('/customer/read_messages/<int:message_id>', methods=['GET','POST'])
@customer_required
def read_messages(message_id):

    db.query(QUERY.UPDATE_MESSAGE_READ_FROM_LV1.format(message_id))
    return redirect(url_for('customer.get_messages'))

# Customer sends response message to the lv1 users
@customer_bp.route('/customer/send_messages', methods=['GET','POST'])
@customer_required
def send_messages_to_lv1():
    cus_messages = session.get('cus_messages', [])

    if request.method == 'POST':
       
        if 'message_subject' in request.form:
            message_subject = request.form['message_subject']
        else:
            return "Missing message subject", 400
        if 'message_content' in request.form:
            message_content = request.form['message_content']
        else:
            return "Missing message content", 400
        
        user_id = session['user_id']
        message_timestamp = datetime.now()

        try:
            new_message_id = db.querywithLastID(QUERY.INSERT_MESSAGES_TO_LV1.format(user_id, message_subject))

            db.querywithLastID(QUERY.INSERT_MESSAGES_CONTENTS_TO_LV1.format(new_message_id, message_content, message_timestamp))
            flash('Your message is delivered to the team!', 'success')
            order_id = request.form.get('order_id')
            if order_id:
                 return redirect(url_for('customer.customer_order_details', id = order_id ))
            return render_template('customer/contact.html')
        except Exception as e:
            flash(f"Error in sending messages: {e}", 'danger')
    if request.method == 'GET':
        return render_template('customer/contact.html', cus_messages=cus_messages)
    

# View Customer Credit
@customer_bp.route('/customer/customer_credit', methods=['GET'])
@customer_required
def customer_credit():
    user_id = session['user_id']
    
    cus_messages = session.get('cus_messages', [])

    credit_limit_result = db.queryOneResult(QUERY.GET_CUSTOMER_CREDIT_LIMIT.format(user_id))
    credit_limit = credit_limit_result.get('credit_limit') if credit_limit_result else 0

    credit_used_result = db.queryOneResult(QUERY.GET_CREDIT_USED_BY_USER.format(user_id))
    credit_used = credit_used_result.get('credit_used') if credit_used_result else 0
    if credit_used:
    
        remaining_credit = credit_limit - credit_used
    else:
        remaining_credit = credit_limit

    
    return render_template('customer/customer_credit.html', credit_limit=credit_limit, remaining_credit=remaining_credit, cus_messages=cus_messages)

# Apply for Credit Limit Increase
@customer_bp.route('/customer/apply_credit_limit', methods=['POST'])
@customer_required
def apply_credit_limit():
    user_id = session['user_id']
    new_credit_limit = request.form['new_credit_limit']
    reason = request.form.get('reason')
    message_content = f""" Reason: {reason}
    Monthly Limit applied: {new_credit_limit}
    """
    create_new_message = QUERY.SET_ACCOUNT_HOLDER_APPLICATION_TO_MESSAGE.format(user_id, 'Apply for Increase in Credit Limit')
    message_id = db.querywithLastID(create_new_message)

    create_new_message_content = QUERY.SET_ACCOUNT_HOLDER_APPLICATION_TO_MESSAGE_CONTENT.format(message_id, message_content, datetime.now())

    db.query(create_new_message_content)
    
    flash('Your request to increase the credit limit has been submitted.', 'success')
    return redirect(url_for('customer.customer_credit'))


@customer_bp.route('/customer/rewards', methods=['GET','POST'])
@customer_required
def checkRewards():

    cus_messages = session.get('cus_messages', [])

    reward_points = db.query(QUERY.GET_REWARD_POINTS)
    user_id = session['user_id']
    current_point = db.queryOneResult(QUERY.GET_CUSTOMER_PROFILE.format(user_id))['points']
    next_level_point = None
    next_level_reward = None
    for r in reward_points:
        if r['level_point'] >= current_point:
            next_level_point = r['level_point']
            next_level_reward = r['gift_card_amount']
            break

    if request.method == 'POST':
        point = int(request.form.get('point'))
        
        validate = False
        for r in reward_points:
            if r['level_point'] == point:
                validate = True
                amount = r['gift_card_amount']
                break

        if current_point >= point and validate:
            gift_card_id = generateGiftCard(amount, 'reward', user_id)
            db.query(QUERY.INSERT_NEW_USER_POINTS_REWARD_HISTORY.format(user_id, gift_card_id, amount,  datetime.today() ))
            db.query(QUERY.UPDATE_USER_POINTS_BY_ID.format(current_point - point, user_id)) 
            flash('Giftcard redeemed, please check your inbox and register in the Giftcard Center.', 'success')
        else:
            flash("Error redeeeming giftcard!", 'danger')
        return redirect(url_for('customer.checkRewards'))
    
    # max_point_history = db.queryOneResult(QUERY.GET_MAX_USER_POINTS_BY_ID.format(user_id)).get('p')
    # if max_point_history and max_point_history > current_point:
    #     for reward in reward_points:
    #         if reward['level_point'] > max_point_history :
    #             return render_template('customer/rewards.html', current_point = current_point, reward = reward )
      
    # else:
    #     for reward in reward_points:
    #         if reward['level_point'] > current_point :
    #             return render_template('customer/rewards.html', current_point = current_point, reward = reward )

    return render_template('customer/rewards.html', current_point = current_point, reward_points = reward_points, next_level_point = next_level_point, next_level_reward = next_level_reward, cus_messages=cus_messages)




@customer_bp.route('/customer/giftcard_center')
@customer_required

def giftcardCenter():


    cus_messages = session.get('cus_messages', [])

    user_id = session['user_id']
    cards =  db.query(QUERY.GET_CUSTOMER_GIFT_CARD_HISTORY.format(user_id))
    today = date.today()

    return render_template('customer/giftcard_history.html', cards = cards, today = today, cus_messages=cus_messages)


# leave review for product detail
@customer_bp.route('/customer/leaveReview', methods=['POST'])
@customer_required
def leave_review():
    user_id = session['user_id']
    product_id = request.form.get('product_id')
    rating = request.form.get('rating')
    content = request.form.get('content')
    query = QUERY.LEAVE_NEW_REVIEW.format(user_id, product_id,rating, content,  date.today() )
    db.query(query)
    flash('Review success!', 'success')
    return redirect(url_for('customer.customer_products', id = product_id ))


@customer_bp.route('/customer/giftcard_center/registerNewGiftcard', methods=['POST'])
@customer_required
def registerNewGiftcard():
    user_id = session['user_id']
    cardnumber = request.form.get('cardnumber')
    giftcard = db.queryOneResult(QUERY.GET_COUPON.format(cardnumber ))
    if not giftcard or giftcard['user_id']:
        flash('Giftcard does not exist!', 'danger')
  
    else:
        db.query(QUERY.REGISTER_GIFTCARD_TO_ONE_CUSTOMER.format( user_id, giftcard['gift_card_id'] ))
        flash('Giftcard registered!', 'success')
    return redirect(url_for('customer.giftcardCenter' ))



# Customer View Promotion Products
@customer_bp.route('/customer/promotion/')

def customer_promotions():
    print('{timestamp} -- customer promotion page request started'.format(timestamp=datetime.utcnow().isoformat()))
    promotions = db.query(QUERY.GET_PROMOTION_LIST)
  
    updatePromotionStatus()
    
    products = db.query(QUERY.GET_ALL_PRODUCTS)
    categories = db.query(QUERY.GET_ALL_CATEGORIES)
    subcategories = db.query(QUERY.GET_ALL_SUBCATEGORIES)
    promotion_products = []
    subcategories_in_promotion = db.query(QUERY.GET_ALL_PROMOTION_SUBCATOGERIES_TO_VERIFY)  
    products_in_promotion = db.query(QUERY.GET_ALL_PROMOTION_PRODUCTS_TO_VERIFY)  
    categories_in_promotion = db.query(QUERY.GET_ALL_PROMOTION_CATOGERIES_TO_VERIFY) 

    for i, product in enumerate(products):
        if verifyProductInPromotion(subcategories_in_promotion,products_in_promotion, categories_in_promotion, product['product_id'], product['subcategory_id']):
            discountedPrice = get_price_after_discount(product['product_id'], product['product_price'], 2)
            if discountedPrice: 
                products[i]['discounted_price'] = discountedPrice
                promotion_products.append(product)
    print('{timestamp} -- customer promotion page request ended'.format(timestamp=datetime.utcnow().isoformat()))

    return render_template('customer/promotion_products.html', products=promotion_products,  promotions=promotions, categories = categories,subcategories = subcategories )
