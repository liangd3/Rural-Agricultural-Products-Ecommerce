from functools import wraps
from flask import redirect, session, flash
from datetime import datetime, timedelta
import os
from flask import current_app
import uuid
from flask import Flask, request, abort
from flask_hashing import Hashing
import db.queryStrings as QUERY
import db.db as db
import re
from random import randint
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
hashing = Hashing(app)

def createSession(user_id, email, role):
    session['loggedin'] = True
    session['user_id'] = user_id
    session['email'] = email
    session['user_type'] = role
    query = QUERY.GET_USER_NAMES.format(user_id)
    account = db.queryOneResult(query)
    session['first_name'] = account['first_name']
    session['last_name'] = account['last_name']
    session['profile_image'] = account['profile_image']
    return

def removeSession():
    
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('email', None)
    session.pop('user_type', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    session.pop('profile_image', None)
    session.pop('cus_messages', None)
    session.pop('credit_limit', None)
    return

   

# Decorator function to protect login required routes
# if is logged in, continue current funciton
# if is not logged in, redirect to login route
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isAuthenticated() == False:
            flash('Please login first!')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
    
        if isAuthenticated() == False:
            flash('Please login first!')
            return redirect('/login')
        if session['user_type'] != 'customer':
            flash('Unauthorized User!')
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
       
        if isAuthenticated() == False:
            flash('Please login first!')
            return redirect('/login')
        if session['user_type'] != 'staff':
            flash('Unauthorized User!')
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function


def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if isAuthenticated() == False:
            flash('Please login first!')
            return redirect('/login')
        if session['user_type'] != 'manager':
            flash('Unauthorized User!')
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isAuthenticated() == False:
            flash('Please login first!')
            return redirect('/login')
        if session['user_type'] != 'admin':
            flash('Unauthorized User!')
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function

# Check before functions for internal use, allows access for staff, manager and admin
def level_one_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isAuthenticated() == False:
            flash('Please login first!')
            return redirect('/login')
        if session['user_type'] != 'staff' and session['user_type'] != 'manager' and session['user_type'] != 'admin':
            flash('Unauthorized User!')
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function

# Check before functions for higher level internal use, allows access for only manager and admin, but does not allow staff access
def level_two_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if isAuthenticated() == False:
            flash('Please login first!')
            return redirect('/login')
        if session['user_type'] != 'manager' and session['user_type'] != 'admin':
            flash('Unauthorized User!')
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated_function



def uploadImage(request):
    # Check if image file is present in the request
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    # Check if file name is provided
    if file.filename == '':
        return 'No selected file'
    if file:
        # Define upload folder and save file
        UPLOAD_FOLDER = 'static/images'
        current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        filename = file.filename
        # Generate unique filename using UUID
        index = filename.rfind('.')
        substring = filename[index:]
        filename = uuid.uuid4().hex + substring
        basedir = os.path.abspath(os.path.dirname(__file__))
        file.save(os.path.join(basedir, current_app.config['UPLOAD_FOLDER'], filename))
        return filename


# Helper function to check if user is authenticated
def isAuthenticated():
    return 'user_id' in session

# convert dateimte db format to datetime-local frontend format
def dateTimeToDateTimeLocal(datetime):
    return datetime.strftime('%Y-%m-%dT%H:%M')

# convert datetime-local from frontend to db datetime format
def dateTimeLocalToDatetime(date, time):
    datetimeStr = f"{date} {time}"
    newDateTime = datetime.strptime(datetimeStr, '%Y-%m-%d %H:%M:%S')
    formatted = newDateTime.strftime('%Y-%m-%d %H:%M:%S')
    return formatted

# check if given datetime is in the past
def isPastDateTime(dateTime):
     print(dateTime)
     standardDateTime = datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
     return standardDateTime < datetime.now()

def changePasswordFunction(input_password):
    saltBytes = uuid.uuid4().bytes
    salt = saltBytes.hex()
    return hashing.hash_value(input_password, salt), salt


def checkPassword(user_password, input_password, user_salt):
    if hashing.check_value(user_password, input_password, user_salt):
        return True
    return False

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def updatePromotionStatus():
    promotions_list = db.query("SELECT * FROM Promotions")

    for promotion in promotions_list:
        if promotion['status'] != "Deleted":
            if promotion['start_date'] <= datetime.now() <= promotion['end_date']:
                promotion['status'] = "Active"
            elif (promotion['start_date'] <= datetime.now() + timedelta(days = 7)) and (promotion['end_date'] > datetime.now()):
                promotion['status'] = "Coming Soon"
            elif promotion['start_date'] > datetime.now() + timedelta(days = 7):
                promotion['status'] = "Inactive"
            elif promotion['end_date'] < datetime.now():
                promotion['status'] = "Expired"
            db.query(QUERY.UPDATE_PROMOTION_STATUS.format(promotion['status'], promotion['promotion_id']))



def sendMessage(user_id, message_subject, message_content):
        if session['user_type'] and session['user_type'] != 'customer':
            
            messageId = db.querywithLastID(QUERY.SEND_MESSAGE.format(user_id, message_subject))
            db.query(QUERY.SEND_MESSAGE_CONTENT.format(messageId, message_content,datetime.now(), session['user_id'] ))
       
        return

def get_price_after_discount(productID, oldPrice, qty):
    updatePromotionStatus()

    categoryPromo = db.queryOneResult(QUERY.GET_RELATED_CATEGORY_PROMO_BY_PRODUCT.format(productID))
    subcategoryPromo = db.queryOneResult(QUERY.GET_RELATED_SUBCATEGORY_PROMO_BY_PRODUCT.format(productID))
    productPromo = db.queryOneResult(QUERY.GET_RELATED_PRODUCT_PROMO_BY_PRODUCT.format(productID))

    categoryBogof = db.queryOneResult(QUERY.GET_BOGOF_CATEGORY_PROMO_BY_PRODUCT.format(productID))
    subcategoryBogof = db.queryOneResult(QUERY.GET_BOGOF_SUBCATEGORY_PROMO_BY_PRODUCT.format(productID))
    productBogof = db.queryOneResult(QUERY.GET_BOGOF_PRODUCT_PROMO_BY_PRODUCT.format(productID))

    newPrice = oldPrice * (1 - max(categoryPromo['discount_rate'] if categoryPromo['discount_rate'] else 0, \
                            subcategoryPromo['discount_rate'] if subcategoryPromo['discount_rate'] else 0, \
                            productPromo['discount_rate'] if productPromo['discount_rate'] else 0))
    priceIfBogof = oldPrice * ((qty // 2) + qty % 2)

    if (categoryPromo['discount_rate'] == None and subcategoryPromo ['discount_rate'] == None and productPromo['discount_rate'] == None):
        return None
    elif (categoryBogof or subcategoryBogof or productBogof) and (priceIfBogof <= newPrice * qty):
        return "buyOneGetOneFree"
    else:
        return round(newPrice,2)




# Function to update customer point when make payment, and issue a new gift card when certain level achieved
# Need an interger for payment amout
def updateCustomerPoints(paymentAmount, user_id):
    
    past_point = db.queryOneResult(QUERY.GET_CUSTOMER_PROFILE.format(user_id))['points']
    # max_point_history = db.queryOneResult(QUERY.GET_MAX_USER_POINTS_BY_ID.format(user_id)).get('p')
    # reward_points = db.query(QUERY.GET_REWARD_POINTS)
    current_point = past_point + paymentAmount

    # if max_point_history and max_point_history > current_point:
    #     for reward in reward_points:
    #         if reward['level_point'] <= current_point and reward['level_point'] > max_point_history:
    #             #generate gift card
    #             gift_card_id = generateGiftCard(reward['gift_card_amount'], user_id)
    #             db.query(QUERY.INSERT_NEW_USER_POINTS_REWARD_HISTORY.format(user_id, gift_card_id,reward['level_point'], datetime.today() ))          
    #         else:  
    #             break
      
    # elif max_point_history:
    #       for reward in reward_points:
    #         if reward['level_point'] <= current_point and reward['level_point'] > max_point_history:
    #             #generate gift card
    #             gift_card_id = generateGiftCard(reward['gift_card_amount'], user_id)
    #             db.query(QUERY.INSERT_NEW_USER_POINTS_REWARD_HISTORY.format(user_id, gift_card_id,reward['level_point'], datetime.today() ))
            

    # else:
    #     for reward in reward_points:
    #         if reward['level_point'] <= current_point:
    #             #generate gift card
    #             gift_card_id = generateGiftCard(reward['gift_card_amount'], user_id)
    #             db.query(QUERY.INSERT_NEW_USER_POINTS_REWARD_HISTORY.format(user_id, gift_card_id,reward['level_point'], datetime.today() ))
    #         else:
    #             break
    
    db.query(QUERY.UPDATE_USER_POINTS_BY_ID.format(current_point, user_id))            
    return True



def generateGiftCard(amount, source, user_id ):
    gift_card_number = str(randint(1,9))
    for i in range(15):
        gift_card_number = gift_card_number + str(randint(0,9))
    expiry_date = datetime.today() +  relativedelta(years=3)
    gift_card_id = db.querywithLastID(QUERY.INSERT_NEW_GIFT_CARD.format(gift_card_number, amount, source, expiry_date ))    
    message_subject = 'New gift card'
    message_content = f'Congratulations, you have just earned a new gift card! The gift card number is: {gift_card_number}, please note your gift card will expire after three years, which is {expiry_date}.'
    messageId = db.querywithLastID(QUERY.SEND_MESSAGE.format(user_id, message_subject))
    db.query(QUERY.SEND_MESSAGE_CONTENT.format(messageId, message_content,datetime.now(), 1 ))
    
    return gift_card_id


# call the function to avoid unnecessary database usage, with examples of necessary parameters
def verifyProductInPromotion(subcategories, products, categories, product_id, subcategory_id):
    # subcategories = db.query(QUERY.GET_ALL_PROMOTION_SUBCATOGERIES_TO_VERIFY)  
    for s in subcategories:
        if s['subcategory_id'] == subcategory_id:
            return True

    # products = db.query(QUERY.GET_ALL_PROMOTION_PRODUCTS_TO_VERIFY)  
    for p in products:
        if p['product_id'] == product_id:
            return True

    # categories = db.query(QUERY.GET_ALL_PROMOTION_CATOGERIES_TO_VERIFY)  
    for c in categories:
        if c['subcategory_id'] == subcategory_id:
            return True
    return False


