from flask import Blueprint, flash, render_template, session, request
from util.util import login_required, staff_required
import db.queryStrings as QUERY
import db.db as db


staff_bp = Blueprint('staff',__name__,template_folder='templates')


# Staff Dashboard
@staff_bp.route('/staff')
@staff_required
def staff_dashboard():

    query = QUERY.FIND_A_STAFF_BY_ID.format(session['user_id'])
    staff_dict = db.queryOneResult(query)
    staff = list(staff_dict.values())
    product_count = db.queryOneResult(QUERY.PRODUCT_COUNT)['count(product_id)']
    active_product_count = db.queryOneResult(QUERY.ACTIVE_PRODUCT_COUNT)['count(product_id)']
    inactive_product_count = db.queryOneResult(QUERY.INACTIVE_PRODUCT_COUNT)['count(product_id)']
    this_month_order_count = db.queryOneResult(QUERY.CURRENT_MONTH_ORDERS_COUNT)['current_month_orders']
    last_month_order_count = db.queryOneResult(QUERY.LAST_MONTH_ORDERS_COUNT)['previous_month_orders']
    new_message_count = db.queryOneResult(QUERY.NEW_MESSAGE_COUNT)['count(message_id)']
    orders = db.query(QUERY.GET_ALL_ORDERS)

    return render_template('staff/staff_dashboard.html', staff=staff, product_count=product_count,active_product_count=active_product_count, inactive_product_count=inactive_product_count, 
                           this_month_order_count=this_month_order_count, last_month_order_count=last_month_order_count, new_message_count=new_message_count, orders = orders)

# Staff Profile
@staff_bp.route('/staff/profile')
@staff_required
def staff_profile():
    query = QUERY.GET_STAFF_PROFILE.format(session['user_id'])
    profile = db.queryOneResult(query)
    return render_template('staff/staff_profile.html', profile = profile)

@staff_bp.route('/staff/profile/edit', methods = ['GET', 'POST'])
@staff_required
def staff_profile_edit():
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
        db.query(QUERY.EDIT_STAFF_PROFILE.format(firstName, lastName, phone ,session['user_id']))
        query = QUERY.GET_STAFF_PROFILE.format(session['user_id'])
        profile = db.queryOneResult(query)
        session['first_name'] = firstName
        session['last_name'] = lastName
        flash('Profile updated sucssesfully.', 'success')
    return render_template('staff/staff_profile.html', profile = profile)
