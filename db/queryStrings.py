# User queries


# get a user by email
FIND_A_USER_BY_EMAIL = 'SELECT * FROM Users WHERE email_address="{}";'


# get a user by id
FIND_A_USER_BY_ID = 'SELECT * FROM Users WHERE user_id="{}";'


# Register a new user
REGISTER_A_NEW_USER = """INSERT INTO Users (email_address, password, salt)   VALUES("{}","{}","{}");"""


# Register a new user - staff type
REGISTER_A_NEW_USER_STAFF_TYPE = """INSERT INTO Users (email_address, password, salt, user_type)   VALUES("{}","{}","{}","{}");"""


# Register a new customer after user successfully registered
REGISTER_A_NEW_CUSTOMER = """INSERT INTO Customers (user_id, register_date, credit_limit)   VALUES("{}", "{}", {});"""

# get a manager by session id
FIND_A_MANAGER_BY_ID = 'SELECT * FROM Managers WHERE user_id="{}";'

# get a staff by session id
FIND_A_STAFF_BY_ID = 'SELECT * FROM Staff WHERE user_id="{}";'

# get a admin by session id
FIND_A_ADMIN_BY_ID = 'SELECT * FROM Admins WHERE user_id="{}";'

# Get profiles
GET_MANAGER_PROFILE = 'SELECT first_name, last_name, profile_image, phone, email_address FROM Managers INNER JOIN Users ON Managers.user_id = Users.user_id WHERE Managers.user_id="{}";'
GET_CUSTOMER_PROFILE = 'SELECT first_name, last_name, profile_image, phone, email_address, points, credit_limit, address_id FROM Customers INNER JOIN Users ON Customers.user_id = Users.user_id WHERE Customers.user_id="{}";'
GET_STAFF_PROFILE = 'SELECT first_name, last_name, profile_image, phone, email_address FROM Staff INNER JOIN Users ON Staff.user_id = Users.user_id WHERE Staff.user_id="{}";'
GET_ADMIN_PROFILE = 'SELECT first_name, last_name, profile_image, phone, email_address FROM Admins INNER JOIN Users ON Admins.user_id = Users.user_id WHERE Admins.user_id="{}";'

# Edit profile
EDIT_MANAGER_PROFILE = 'UPDATE Managers SET first_name = "{}", last_name = "{}", phone = "{}" WHERE user_id="{}";'
EDIT_CUSTOMER_PROFILE = 'UPDATE Customers SET first_name = "{}", last_name = "{}", phone = "{}" WHERE user_id="{}";'
EDIT_STAFF_PROFILE = 'UPDATE Staff SET first_name = "{}", last_name = "{}", phone = "{}" WHERE user_id="{}";'
EDIT_ADMIN_PROFILE = 'UPDATE Admins SET first_name = "{}", last_name = "{}", phone = "{}" WHERE user_id="{}";'

# Get current password detail
GET_CURRENT_PASSWORD = 'SELECT password, salt FROM Users WHERE user_id = "{}";'

# Update password
UPDATE_PASSWORD = 'UPDATE Users SET password = "{}", salt = "{}" WHERE user_id = "{}";'

# Get user's first, last name and profile image
GET_USER_NAMES = 'SELECT * FROM (SELECT first_name, last_name, profile_image, user_id FROM Managers \
                    UNION SELECT first_name, last_name, profile_image, user_id FROM Admins \
                    UNION SELECT first_name, last_name, profile_image, user_id FROM Customers \
                    UNION SELECT first_name, last_name, profile_image, user_id FROM Staff) AS u \
                    WHERE u.user_id = "{}";'

# Get profile image path
GET_PROFILE_IMAGE_PATH = 'SELECT * FROM (SELECT profile_image, user_id FROM Managers \
                    UNION SELECT profile_image, user_id FROM Admins \
                    UNION SELECT profile_image, user_id FROM Customers \
                    UNION SELECT profile_image, user_id FROM Staff) AS u \
                    WHERE u.user_id = "{}";'

# Delete Profile Image (Reset to default)
DELETE_PROFILE_IMAGE = 'UPDATE {} SET profile_image = "default-image.jpg" WHERE user_id = "{}";'

# Set profile image path
SET_PROFILE_IMAGE = 'UPDATE {} SET profile_image = "{}" WHERE user_id = "{}";'

# set account holder application to message 
SET_ACCOUNT_HOLDER_APPLICATION_TO_MESSAGE = "INSERT INTO Messages (user_id, message_subject) VALUES ({},'{}');"

# set account holder application detail to message content 
SET_ACCOUNT_HOLDER_APPLICATION_TO_MESSAGE_CONTENT = "INSERT INTO Message_Contents (message_id, message_content, message_timestamp) VALUES ({},'{}','{}');"

# Get promotion list
GET_PROMOTION_LIST = 'SELECT * FROM Promotions WHERE status != "Deleted" and status != "Expired"  ORDER BY promotion_id ASC;'

# Update promotion status
UPDATE_PROMOTION_STATUS = 'UPDATE Promotions SET status = "{}" WHERE promotion_id = "{}";'

# Get promotion detail
GET_PROMOTION_DETAIL = 'SELECT * FROM Promotions WHERE promotion_id = "{}";'
GET_PROMOTION_CATAGORIES = 'SELECT c.category_id, c.category_name FROM Promotion_Categories AS pc JOIN Categories AS c ON pc.category_id = c.category_id WHERE promotion_id = "{}" ;'
GET_PROMOTION_SUBCATAGORIES = 'SELECT s.subcategory_id, s.subcategory_name FROM Promotion_Subcategories AS ps JOIN Subcategories AS s ON ps.subcategory_id = s.subcategory_id WHERE promotion_id = "{}" ;'
GET_PROMOTION_PRODUCTS = 'SELECT p.product_id, p.product_name FROM Promotion_Products AS pp JOIN Products AS p ON pp.product_id = p.product_id WHERE promotion_id = "{}" ;'




# Get categories excludes giftcard
GET_ALL_CATEGORIES_EXCLUDES_GIFTCARD = 'SELECT * FROM Categories WHERE category_id != 1;'

# Get subcategories excludes giftcard
GET_ALL_SUBCATEGORIES_EXCLUDES_GIFTCARD = 'SELECT * FROM Subcategories WHERE subcategory_id != 1;'

# Get products excludes giftcard
GET_ALL_PRODUCTS_EXCLUDES_GIFTCARD = 'SELECT * FROM Products WHERE product_status = 1 AND subcategory_id != 1;'


# Get subcategories excludes giftcard
GET_ALL_SUBCATEGORIES_EXCLUDES_GIFTCARD_BY_ID = 'SELECT * FROM Subcategories WHERE category_id = "{}";'

# Get products excludes giftcard
GET_ALL_PRODUCTS_EXCLUDES_GIFTCARD_BY_SUBCAT_ID = 'SELECT * FROM Products WHERE product_status = 1 AND subcategory_id = "{}";'
GET_ALL_PRODUCTS_EXCLUDES_GIFTCARD_BY_CAT_ID = '''SELECT * FROM Products p
                                                    LEFT JOIN Subcategories s ON p.subcategory_id = s.subcategory_id
                                                    WHERE p.product_status = 1 AND s.category_id = "{}";'''




# Get categories
GET_ALL_CATEGORIES = 'SELECT * FROM Categories;'

# Get subcategories
GET_ALL_SUBCATEGORIES = 'SELECT * FROM Subcategories;'

# Get products
GET_ALL_PRODUCTS = 'SELECT * FROM Products p LEFT JOIN Product_Images pi on p.product_image_id = pi.product_image_id WHERE product_status = 1;'

GET_ALL_PRODUCTS_WITH_SUBCATEGORY_ID = 'SELECT * FROM Products p LEFT JOIN Product_Images pi on p.product_image_id = pi.product_image_id WHERE product_status = 1 and subcategory_id = "{}";'

SEARCH_ALL_PRODUCTS_WITH_NAME = 'SELECT * FROM Products p LEFT JOIN Product_Images pi on p.product_image_id = pi.product_image_id WHERE product_status = 1 and product_name LIKE "{}";'
SEARCH_ALL_PRODUCTS_WITH_NAME_AND_SUBCATEGORY_ID = 'SELECT * FROM Products p LEFT JOIN Product_Images pi on p.product_image_id = pi.product_image_id WHERE product_status = 1 and p.subcategory_id = {} and product_name LIKE "{}";'

# Get hot products
GET_HOT_PRODUCTS = '''
SELECT 
    SUM(od.quantity) AS total_quantity_sold,
    p.product_id, p.product_name, p.product_description, p.product_price, p.subcategory_id, p.stock_quantity, p.product_image_id, p.oversized, p.product_status, pi.product_image_id, pi.product_image
FROM 
    Orders o
    NATURAL JOIN Order_Details od
    NATURAL JOIN Products p
    LEFT JOIN Product_Images pi on p.product_image_id = pi.product_image_id
WHERE 
    YEAR(order_date) = YEAR(CURRENT_DATE)
    AND stock_quantity >= 50 AND product_status = 1
GROUP BY 
    product_id, product_name
ORDER BY
    total_quantity_sold DESC
LIMIT 20;





'''

# Get products Images
GET_ALL_PRODUCTS_IMAGES = 'SELECT * FROM Product_Images;'

# Delete promotion (deleted status)
DELETE_PROMOTION = 'UPDATE Promotions SET status = "Deleted" WHERE promotion_id = "{}";'

# Update promotion
UPDATE_PROMOTION = 'UPDATE Promotions SET promotion_name = "{}", promotion_description = "{}", promotion_type = "{}", discount_rate = "{}", special_condition = "{}", start_date = "{}", end_date = "{}" WHERE promotion_id = "{}"'

# Get current promotion type
GET_PROMOTION_TYPE = 'SELECT Promotion_type FROM Promotions WHERE promotion_id = "{}";'

# Update promotion items
CLEAR_PROMOTION_ITEM = 'DELETE FROM Promotion_{} WHERE promotion_id = "{}";'
UPDATE_PROMOTION_ITEM = 'INSERT INTO Promotion_{} VALUES ("{}", "{}");'

# Update discount items
INSERT_DISCOUNT_PRODUCT = 'INSERT INTO Promotion_Products VALUES (1, "{}");'
DELETE_DISCOUNT_PRODUCT = 'DELETE FROM Promotion_Products WHERE promotion_id = 1 AND product_id = "{}";'


# Update promotion image
UPDATE_PROMOTION_IMAGE = 'UPDATE Promotions SET promotion_image = "{}" WHERE promotion_id = "{}";'

# Get promotion image path
GET_PROMOTION_IMAGE_PATH = 'SELECT promotion_image FROM Promotions WHERE promotion_id = "{}";'

# Delete Promotion Image (Reset to default)
DELETE_PROMOTION_IMAGE = 'UPDATE Promotions SET promotion_image = "default-image.jpg" WHERE promotion_id = "{}";'

# New promotion
NEW_PROMOTION = 'INSERT INTO Promotions (promotion_name, promotion_description, promotion_type, discount_rate, special_condition, promotion_image, start_date, end_date)\
                 VALUES ("{}", "{}", "{}", "{}", "{}", "default.jpg","{}", "{}");'

# get all customers details
GET_ALL_CUSTOMERS  = """SELECT Users.user_id, Users.email_address, Users.user_status, Customers.first_name, Customers.last_name, Customers.phone, Customers.profile_image, Customers.points, Customers.credit_limit FROM Customers Natural JOIN Users;"""

# get all staff details
GET_ALL_STAFF  = """SELECT Users.user_id, Users.email_address, Users.user_status, Staff.first_name, Staff.last_name, Staff.phone FROM Staff Natural JOIN Users;"""

# add a new customer
ADD_A_CUSTOMER = 'INSERT INTO Customers (user_id, first_name, last_name, phone) VALUES ("{}","{}","{}","{}");'


# add a new staff
ADD_A_STAFF = 'INSERT INTO Staff (user_id, first_name, last_name, phone ) VALUES ("{}","{}","{}","{}");'

# Deactivate a user by id
DEACTIVATE_USER_BY_ID= 'UPDATE Users set user_status = 0  WHERE user_id = "{}";'

# Activate a user by id
ACTIVATE_USER_BY_ID= 'UPDATE Users set user_status = 1 WHERE user_id = "{}";'

# get customer details by id
GET_CUSTOMER_DETAILS_BY_ID  = """SELECT Users.user_id, Users.email_address, Users.user_status, Customers.first_name, Customers.last_name, Customers.phone, Customers.profile_image, Customers.points, Customers.credit_limit FROM Customers Natural JOIN Users WHERE Users.user_id="{}";"""

# get staff details by id
GET_STAFF_DETAILS_BY_ID  = """SELECT Users.user_id, Users.email_address, Users.user_status, Staff.first_name, Staff.last_name, Staff.phone, Staff.profile_image FROM Staff Natural JOIN Users WHERE Users.user_id="{}";"""


# Update user email address by id
UPDATE_USER_EMAIL_BY_ID = 'UPDATE Users set email_address =  "{}"  WHERE user_id = "{}";'


# Update customer details by id
UPDATE_CUSTOMER_DETAILS_BY_ID  = """UPDATE Customers set  first_name = "{}", last_name = "{}",  phone = "{}"  WHERE user_id = "{}";"""

# Update staff details by id
UPDATE_STAFF_DETAILS_BY_ID  =  """UPDATE Staff set first_name = "{}",   last_name   =  "{}",   phone  =  "{}"  WHERE user_id = "{}";"""





# Update product quantity by id
UPDATE_PRODUCT_QUANTITY_BY_ID  ='''UPDATE Products SET stock_quantity = "{}"  WHERE product_id = "{}";'''


# GET_RELATED_CATEGORY_PROMO_BY_PRODUCTet products with Category
GET_ALL_PRODUCTS_WITH_CATEGORY = '''SELECT  p.product_id, p.product_name, p.product_description, p.product_price, p.subcategory_id, p.stock_quantity, p.product_image_id, p.oversized, p.product_status, 
s.subcategory_name, s.category_id, c.category_name, Product_Images.product_image
FROM Products p LEFT JOIN Subcategories s ON p.subcategory_id = s.subcategory_id LEFT JOIN Categories c ON s.category_id = c.category_id LEFT JOIN Product_Images  ON p.product_image_id = Product_Images.product_image_id WHERE p.subcategory_id != 1;'''


# Get product details
GET_PRODUCT_DATAILS_BY_ID = 'SELECT  * FROM Products NATURAL JOIN Subcategories  NATURAL JOIN Categories WHERE product_id = {};'


# Get product images
GET_PRODUCT_IMAGES_BY_ID = 'SELECT * FROM Product_Images WHERE product_id = {};'


# Activate a product by id
ACTIVATE_A_PRODUCT_BY_ID  ='''UPDATE Products SET product_status = 1  WHERE product_id = "{}";'''

# Inactivate a product by id
INACTIVATE_A_PRODUCT_BY_ID  ='''UPDATE Products SET product_status = 0  WHERE product_id = "{}";'''


# Update product detail by id
UPDATE_PRODUCT_DETAIL_BY_ID  ='''UPDATE Products SET product_name = "{}", product_description = "{}", product_price = "{}", subcategory_id = "{}", oversized = "{}", stock_quantity = "{}"  WHERE product_id = "{}";'''


# Get product detail for editing
GET_PRODUCT_DETAIL = 'SELECT * FROM Products p \
                        LEFT JOIN Subcategories s ON p.subcategory_id = s.subcategory_id \
                        LEFT JOIN Categories c ON s.category_id = c.category_id \
                        WHERE p.product_id = "{}";'

# Get subcategory name from id
GET_SUBCAT_ID_FROM_NAME = 'SELECT subcategory_id FROM Subcategories WHERE subcategory_name = "{}";'

# Update product detail
UPDATE_PRODUCT_DETAIL = 'UPDATE Products SET product_name = "{}", product_description = "{}", product_price = "{}", subcategory_id = "{}", stock_quantity = "{}", oversized = "{}" WHERE product_id = "{}";'

# New product detail
INSERT_PRODUCT = 'INSERT INTO Products (product_name, product_description, product_price, subcategory_id, stock_quantity, oversized, product_status)\
                    VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "1");'


# Get all subcats under a cat
GET_ALL_SUBCATS_FROM_CAT = 'SELECT * FROM Subcategories s JOIN Categories c ON s.category_id = c.category_id WHERE s.category_id = "{}";'

# Set product image path
INSERT_NEW_PRODUCT_IMAGE = 'INSERT INTO Product_Images (product_image, product_id) VALUES ("{}", "{}");'

# Get product image by product ID
GET_PRODUCT_IMAGE_BY_ID = 'SELECT * FROM Product_Images WHERE product_image_id = {};'

# Delete product image from product ID
DELETE_PRODUCT_IMAGE_BY_ID = 'DELETE FROM Product_Images WHERE product_image_id = {};'


# Update Product image
UPDATE_PRODUCT_PRIMARY_IMAGE = 'UPDATE Products SET product_image_id = "{}" WHERE product_id = "{}";'

# Inactive/active product (status = 0)
INACTIVE_PRODUCT = 'UPDATE Products SET product_status = 0 WHERE product_id = "{}";'
ACTIVE_PRODUCT = 'UPDATE Products SET product_status = 1 WHERE product_id = "{}";'

# Get existing product photo count
GET_PRODUCT_IMAGE_COUNT = 'SELECT COUNT(*) count FROM Product_Images WHERE product_id = "{}";'

# Check product primary image by product ID
CHECK_PRODUCT_PRIMARY_IMAGE_BY_ID = 'SELECT product_image_id FROM Products WHERE product_id = {};'

# Check cart quantity
CHECK_CART_QTY = 'SELECT qty FROM Shopping_Carts WHERE user_id = "{}" AND product_id = "{}";'

# Add to cart
PLUS_SOME_TO_CART = 'UPDATE Shopping_Carts SET qty = "{}" WHERE user_id = "{}" AND product_id = "{}";'
INSERT_TO_CART = 'INSERT INTO Shopping_Carts VALUES("{}", "{}", "{}");'

# Get shopping cart
GET_SHOPPING_CART = '''SELECT * FROM Shopping_Carts sc 
                    JOIN Products p ON sc.product_id = p.product_id 
                    JOIN Product_Images pi ON pi.product_image_id = p.product_image_id
                    WHERE sc.user_id = "{}";'''

# Get total cart quantity
GET_SHOPPING_CART_TOTAL_QTY = 'SELECT SUM(qty) AS total FROM Shopping_Carts WHERE user_id = "{}";'

# Get related discounts by product ID
GET_RELATED_CATEGORY_PROMO_BY_PRODUCT = '''SELECT MAX(discount_rate) discount_rate FROM Promotion_Categories pc 
                                            LEFT JOIN Promotions pr ON pc.promotion_id = pr.promotion_id
                                            LEFT JOIN Subcategories s ON pc.category_id = s.category_id
                                            RIGHT JOIN Products p ON s.subcategory_id = p.subcategory_id 
                                            WHERE status = "Active" AND p.product_id = "{}";'''
GET_RELATED_SUBCATEGORY_PROMO_BY_PRODUCT = '''SELECT MAX(discount_rate) discount_rate FROM Promotion_Subcategories ps 
                                                LEFT JOIN Promotions pr ON ps.promotion_id = pr.promotion_id
                                                RIGHT JOIN Products p ON ps.subcategory_id = p.subcategory_id 
                                                WHERE status = "Active" AND p.product_id = "{}";'''
GET_RELATED_PRODUCT_PROMO_BY_PRODUCT = '''SELECT MAX(discount_rate) discount_rate FROM Promotion_Products pp 
                                            LEFT JOIN Promotions pr ON pp.promotion_id = pr.promotion_id
                                            RIGHT JOIN Products p ON pp.product_id = p.product_id 
                                            WHERE status = "Active" AND p.product_id = "{}";'''

# Get Buy One Get One Free discount by ID
GET_BOGOF_CATEGORY_PROMO_BY_PRODUCT = '''SELECT special_condition FROM Promotion_Categories pc 
                                            LEFT JOIN Promotions pr ON pc.promotion_id = pr.promotion_id
                                            LEFT JOIN Subcategories s ON pc.category_id = s.category_id
                                            RIGHT JOIN Products p ON s.subcategory_id = p.subcategory_id 
                                            WHERE status = "Active" AND special_condition LIKE "%buy%" AND p.product_id = "{}";'''
GET_BOGOF_SUBCATEGORY_PROMO_BY_PRODUCT = '''SELECT special_condition FROM Promotion_Subcategories ps 
                                                LEFT JOIN Promotions pr ON ps.promotion_id = pr.promotion_id
                                                RIGHT JOIN Products p ON ps.subcategory_id = p.subcategory_id 
                                                WHERE status = "Active" AND special_condition LIKE "%buy%" AND p.product_id = "{}";'''
GET_BOGOF_PRODUCT_PROMO_BY_PRODUCT = '''SELECT special_condition FROM Promotion_Products pp 
                                            LEFT JOIN Promotions pr ON pp.promotion_id = pr.promotion_id
                                            RIGHT JOIN Products p ON pp.product_id = p.product_id 
                                            WHERE status = "Active" AND special_condition LIKE "%buy%" AND p.product_id = "{}";'''


# Delete an item from cart
DELETE_PRODUCT_FROM_CART = 'DELETE FROM Shopping_Carts WHERE user_id = "{}" AND product_id = "{}";'

# Get user addresses
GET_USER_ADDRESSES = 'SELECT * FROM Addresses WHERE user_id = "{}";'
GET_ADDRESS_BY_ID = 'SELECT * FROM Addresses WHERE address_id = "{}";'

# Get all shipping methods
GET_ALL_SHIPPING = 'SELECT * FROM Shipping_Methods;'

# Get all order + payment history of a user
GET_CREDIT_USED_BY_USER = 'SELECT SUM(payment_amount) AS credit_used FROM Orders JOIN Payments ON Orders.order_id = Payments.order_id WHERE Orders.user_id = "{}" AND payment_type_id = 2;'

# Find a coupon
GET_COUPON = 'SELECT * FROM Gift_Cards WHERE gift_card_number = "{}" AND expiry_date > CURRENT_TIMESTAMP;'

# Get all messages from customers
GET_ALL_MESSAGES_FROM_CUSTOMERS = 'SELECT Messages.user_id, Customers.first_name, Customers.last_name, Users.email_address, Messages.message_id, \
Messages.message_subject, Messages.message_status, Message_Contents.message_content_id, Message_Contents.message_content, \
Message_Contents.message_timestamp, Message_Contents.responder_id FROM Customers \
INNER JOIN Users on Users.user_id = Customers.user_id \
INNER JOIN Messages on Messages.user_id = Users.user_id \
INNER JOIN Message_Contents on Message_Contents.message_id = Messages.message_id \
WHERE Message_Contents.responder_id = 0;'

# Respond messages to customer
GET_SELECTED_MESSAGE_FROM_CUSTOMER = 'SELECT Messages.user_id, Customers.first_name, Customers.last_name, Users.email_address, Messages.message_id,  \
Messages.message_subject, Messages.message_status, Message_Contents.message_content_id, Message_Contents.message_content, \
Message_Contents.message_timestamp, Message_Contents.responder_id FROM Customers \
INNER JOIN Users on Users.user_id = Customers.user_id \
INNER JOIN Messages on Messages.user_id = Users.user_id \
INNER JOIN Message_Contents on Message_Contents.message_id = Messages.message_id \
WHERE Message_Contents.responder_id = 0 AND Messages.message_id = {};'
UPDATE_REPLIED_CUSTOMER_MESSAGE = 'UPDATE Messages SET message_status = 0 WHERE message_id = {};'
INSERT_MESSAGES_TO_CUSTOMER = 'INSERT INTO Messages (user_id, message_subject, message_status) VALUES ("{}", "Re: {}", 1);'
INSERT_MESSAGES_CONTENTS_TO_CUSTOMER = 'INSERT INTO Message_Contents (message_id, message_content, message_timestamp, responder_id) VALUES ("{}", "{}", "{}", "{}");'
SELECT_CREDIT_LIMIT_APPLIED = '''SELECT TRIM( 
            SUBSTRING(
            message_content, 
            LOCATE('Monthly Limit applied:', message_content) + LENGTH('Monthly Limit applied:'),
            LOCATE('\n', message_content, LOCATE('Monthly Limit applied:', message_content)) - (LOCATE('Monthly Limit applied:', message_content) + LENGTH('Monthly Limit applied:'))
            )) AS monthly_limit
FROM 
    Message_Contents
WHERE 
    message_id = {} AND message_content LIKE '%Monthly Limit applied:%';'''
UPDATE_CUSTOMER_CREDIT_LIMIT = 'UPDATE Customers SET credit_limit = {} WHERE user_id = {};'


# Get reviews for one product
GET_PRODUCT_REVIEWS_BY_ID = 'SELECT * FROM Reviews NATURAL JOIN Customers WHERE product_id = "{}";'


# Get all shipping methods
GET_ALL_SHIPPING_METHODS = 'SELECT * FROM Shipping_Methods;'

# Add new shipping method
INSERT_NEW_SHIPPING_METHOD = 'INSERT INTO Shipping_Methods (shipping_name, shipping_price) VALUES("{}", "{}");'

# Update shipping method by ID
UPDATE_SHIPPING_METHOD_BY_ID = 'UPDATE Shipping_Methods SET shipping_name = "{}", shipping_price = "{}" WHERE shipping_method_id = "{}";'

# Delete shipping method by ID(s)
DELETE_SHIPPING_METHOD_BY_ID = 'DELETE FROM Shipping_Methods WHERE shipping_method_id = {};'

# GET shipping method by ID(s)
GET_SHIPPING_METHOD_BY_ID = 'SELECT * FROM Shipping_Methods WHERE shipping_method_id = {};'



# Update address by ID
UPDATE_ADDRESS_BY_ID = 'UPDATE Addresses SET unit_number = "{}", address_line1 = "{}", address_line2 = "{}", region = "{}", city = "{}", postcode = "{}"  WHERE address_id = "{}";'

# Add new address 
ADD_NEW_ADDRESS  = 'INSERT INTO  Addresses  (unit_number, address_line1,address_line2, region, city, postcode, user_id)   VALUES("{}","{}","{}","{}","{}","{}","{}"); '


# Delete address by ID
DELETE_ADDRESS_BY_ID = 'DELETE FROM Addresses WHERE address_id = "{}";'


# Set primary address by ID
SET_PRIMARY_ADDRESS_BY_ID = 'UPDATE Customers SET address_id = "{}"  WHERE user_id = "{}";'



# Delete an item from cart
DELETE_PRODUCT_FROM_CART = 'DELETE FROM Shopping_Carts WHERE user_id = "{}" AND product_id = "{}";'

# Get user addresses
GET_USER_ADDRESSES = 'SELECT * FROM Addresses WHERE user_id = "{}";'
GET_ADDRESS_BY_ID = 'SELECT * FROM Addresses WHERE address_id = "{}";'

# Get all shipping methods
GET_ALL_SHIPPING = 'SELECT * FROM Shipping_Methods;'



# Get all orders
GET_ALL_ORDERS = '''SELECT 
    o.order_id, 
    o.user_id, 
    o.order_date, 
    o.total_amount, 
    o.shipping_method_id, 
    o.order_status, 
    o.processor_id, 
    o.shipping_address,  
    u.user_type, 
    CASE 
        WHEN u.user_type = 'staff' THEN s.first_name
        WHEN u.user_type = 'manager' THEN m.first_name
        WHEN u.user_type = 'admin' THEN a.first_name
    END AS first_name,
    CASE 
        WHEN u.user_type = 'staff' THEN s.last_name
        WHEN u.user_type = 'manager' THEN m.last_name
        WHEN u.user_type = 'admin' THEN a.last_name
    END AS last_name,
    sm.shipping_method_id, 
    sm.shipping_name, 
    sm.shipping_price 
FROM Orders o 
LEFT JOIN Users u ON o.processor_id = u.user_id
LEFT JOIN Staff s ON u.user_type = 'staff' AND s.user_id = u.user_id
LEFT JOIN Managers m ON u.user_type = 'manager' AND m.user_id = u.user_id
LEFT JOIN Admins a ON u.user_type = 'admin' AND a.user_id = u.user_id
LEFT JOIN Shipping_Methods sm ON o.shipping_method_id = sm.shipping_method_id
ORDER BY
    CASE order_status
        WHEN 'paid' THEN 1
        WHEN 'pending' THEN 2
        WHEN 'preparing' THEN 3
        WHEN 'ready' THEN 4
        WHEN 'sent' THEN 5
        WHEN 'placed' THEN 6
        WHEN 'finished' THEN 7
        WHEN 'cancelled' THEN 8
        ELSE 9 
    END;

'''

# Get order detail by id
GET_ORDERS_DETAILS_BY_ID = 'SELECT * FROM Orders o LEFT JOIN Shipping_Methods s ON o.shipping_method_id = s.shipping_method_id WHERE order_id = "{}";'

# Get all products for one order  by id
GET_PRODUCTS_BY_ORDER_ID = '''SELECT * FROM Order_Details o 
LEFT JOIN (SELECT product_id, MIN(product_image_id) AS product_image_id FROM Product_Images GROUP BY product_id ) p ON o.product_id = p.product_id
LEFT JOIN (SELECT product_image_id AS pid, product_image FROM Product_Images) pi ON p.product_image_id = pi.pid
WHERE order_id = "{}"'''

# Get order detail by id
UPDATE_ORDER_STATUS_BY_ID = 'UPDATE Orders  SET order_status = "{}",  processor_id  = "{}" WHERE order_id = "{}";'



# Send message
SEND_MESSAGE = 'INSERT INTO  Messages (user_id, message_subject) VALUES  ("{}","{}"); '
SEND_MESSAGE_CONTENT = 'INSERT INTO  Message_Contents (message_id, message_content, message_timestamp, responder_id) VALUES  ("{}", "{}","{}", {}); '

# Get customer orders
GET_CUSTOMER_ORDERS = 'SELECT order_id, user_id, order_date, total_amount, shipping_method_id, order_status, processor_id, shipping_address FROM Orders WHERE user_id = {};'


# Get customer orders with payment and shipping details
GET_CUSTOMER_ORDERS_WITH_PAYMENTS_AND_SHIPPING = 'SELECT o.order_id, o.user_id, o.order_date, o.total_amount, o.shipping_method_id, o.order_status, o.processor_id, o.shipping_address, p.payment_id,  p.payment_amount,  p.payment_type_id,  p.payment_status,   s.shipping_name, s.shipping_price,  pt.payment_type_name FROM Orders o LEFT JOIN Payments p ON o.order_id =  p.order_id LEFT JOIN Shipping_Methods s ON o.shipping_method_id = s.shipping_method_id LEFT JOIN  Payment_Types pt on p.payment_type_id = pt.payment_type_id       WHERE o.user_id = {} ORDER BY o.order_id DESC;'


GET_PAYMENTS_BY_ORDER_ID = """
SELECT p.payment_id, p.user_id, p.order_id, p.payment_date_time, p.payment_amount, pt.payment_type_name, p.payment_status
FROM Payments p
JOIN Payment_Types pt ON p.payment_type_id = pt.payment_type_id
WHERE p.order_id = {};"""

# Get Order details
GET_ORDER_DETAILS_BY_ORDER_ID = 'SELECT od.product_id, od.quantity, od.unit_price FROM Order_Details od WHERE od.order_id = {};'


# Get Reward Points Settings
GET_REWARD_POINTS = 'SELECT * FROM User_Gift_Card_Points_Level ;'

# Get Current Highest Point
GET_MAX_CUSTOMER_POINT = 'SELECT MAX(points) AS p FROM Customers ;'

# Get Current Highest Point
GET_MAX_REWARD_POINTS = 'SELECT MAX(level_point) AS p  FROM User_Gift_Card_Points_Level ;'


#  Set New Reward Points 
SET_NEW_REWARD_POINTS ='INSERT INTO User_Gift_Card_Points_Level  ( level_point, gift_card_amount) VALUES  ("{}","{}"); '

#  Set New Reward Points 
DELETE_REWARD_LEVEL ='DELETE FROM User_Gift_Card_Points_Level WHERE level_id = "{}" ;'

# Insert a new order
INSERT_NEW_ORDER = '''INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status, shipping_address)
                                  VALUES ("{}", "{}", "{}", "{}", "placed", "{}");'''
# Inserst new order detail
INSERT_ORDER_DETAIL = 'INSERT INTO Order_Details VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}");'

#Insert payment detail
INSERT_PAYMENT = '''INSERT INTO Payments (user_id, order_id, payment_date_time, payment_amount, payment_type_id)
                                    VALUES("{}", "{}", "{}", "{}", "{}");'''
# INSERT_PAYMENT_GIFT_CARD = '''INSERT INTO Payments (user_id, order_id, payment_date_time, payment_amount, payment_type_id, gift_card_id, gift_card_amount)
#                                     VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}");'''

# validate gift card
GET_GIFT_CARD_DETAIL = 'SELECT * FROM Gift_Cards WHERE gift_card_number = "{}";'

# get payment type ID
GET_PAYMENT_TYPE_ID = 'SELECT * FROM Payment_Types WHERE payment_type_name LIKE "{}";'

# update gift card amount
UPDATE_GIFT_CARD_AMOUNT = 'UPDATE Gift_Cards SET gift_card_amount = "{}" WHERE gift_card_number = "{}";'


# insert new address
INSERT_NEW_ADDRESS = '''INSERT INTO Addresses (user_id, unit_number, address_line1, address_line2, city, region, postcode)
                                        VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}")'''

# Get shipping method ID
GET_SHIPPING_METHOD_ID = 'SELECT shipping_method_id, shipping_price WHERE shipping_method_id; '

# get customer detail
GET_CUSTOMER_DETAIL = 'SELECT * FROM Customers c JOIN Users u ON c.user_id = u.user_id WHERE c.user_id = "{}";'

#  Get All User Points History
GET_ALL_USER_POINTS_BY_ID ='SELECT * FROM User_Gift_Card_Records WHERE user_id = {};'


#  Get Highest User Points History
GET_MAX_USER_POINTS_BY_ID ='SELECT MAX(level_point) AS p FROM User_Gift_Card_Records WHERE user_id = {};'

#  Update user point after payment
UPDATE_USER_POINTS_BY_ID ='UPDATE Customers  SET points = "{}" WHERE user_id = "{}";'


#  Inser new User Points History
INSERT_NEW_USER_POINTS_REWARD_HISTORY = 'INSERT INTO  User_Gift_Card_Records (user_id,   gift_card_id,  level_point,  record_date) VALUES  ("{}","{}","{}","{}"); '


#  Inser new Gift Card
INSERT_NEW_GIFT_CARD = 'INSERT INTO  Gift_Cards (gift_card_number ,    gift_card_amount ,    source,   expiry_date ) VALUES  ("{}","{}","{}","{}"); '


# Get all messages from lv1 users
GET_ALL_MESSAGES_FROM_LV1 = '''SELECT 
    Messages.user_id, 
    Messages.message_id,
    Messages.message_subject, 
    Messages.message_status, 
    Message_Contents.message_content_id, 
    Message_Contents.message_content,
    Message_Contents.message_timestamp, 
    Message_Contents.responder_id 
FROM 
    Users
INNER JOIN Messages ON Messages.user_id = Users.user_id
INNER JOIN Message_Contents ON Message_Contents.message_id = Messages.message_id
WHERE Messages.user_id = {} AND Message_Contents.responder_id != 0 AND Message_Contents.responder_id < 10000;'''
UPDATE_MESSAGE_READ_FROM_LV1 = 'UPDATE Messages SET message_status = 0 WHERE message_id = {};'

# Send messages to lv1 users
INSERT_MESSAGES_TO_LV1 = 'INSERT INTO Messages (user_id, message_subject, message_status) VALUES ("{}", "{}", 1);'
INSERT_MESSAGES_CONTENTS_TO_LV1 = 'INSERT INTO Message_Contents (message_id, message_content, message_timestamp, responder_id) VALUES ("{}", "{}", "{}", 0);'

# Delete all products in cart
DELETE_ALL_ITEM_IN_CART = 'DELETE FROM Shopping_Carts WHERE user_id = "{}";'


# Categories and subcategories
GET_ALL_CATEGORIES_AND_SUBCATEGORIES = '''SELECT * FROM Categories
LEFT JOIN Subcategories ON Subcategories.category_id = Categories.category_id;'''
INSERT_NEW_CATEGORY = 'INSERT INTO Categories (category_name) VALUES ("{}");'
INSERT_NEW_SUBCATEGORY = 'INSERT INTO Subcategories (subcategory_name, category_id) VALUES ("{}", {});'
UPDATE_CATEGORY_BY_ID = 'UPDATE Categories SET category_name = "{}" WHERE category_id = {};'
UPDATE_SUBCATEGORY_BY_ID = 'UPDATE Subcategories SET subcategory_name = "{}" WHERE subcategory_id = {};'

# Get customer credit limit
GET_CUSTOMER_CREDIT_LIMIT = "SELECT credit_limit FROM Customers WHERE user_id = {};"


# Get customer gift card history
GET_CUSTOMER_GIFT_CARD_HISTORY = "SELECT * FROM Gift_Cards WHERE user_id = {} ORDER BY gift_card_id DESC;"


# Get all accountholders
GET_ALL_ACCOUNTHOLDERS = "SELECT * FROM Customers WHERE credit_limit > 0.00 ;"

# Get all accountholders
UPDATE_ACCOUNTHOLDER_CREDIT_LIMIT = 'UPDATE Customers  SET credit_limit = "{}" WHERE user_id = "{}";'



# Get customers payment
GET_CUSTOMERS_OVERDUE_PAYMENT = '''SELECT o.user_id, c.first_name, c.last_name, 
       SUM(o.total_amount) AS total_amount, 
       COUNT(o.order_id) AS order_count,
       COUNT(CASE WHEN o.order_date < DATE_FORMAT(NOW() - INTERVAL DAY(NOW()) - 20 DAY, '%Y-%m-21') THEN 1 END) AS overdue_orders_count,
       SUM(CASE WHEN o.order_date < DATE_FORMAT(NOW() - INTERVAL DAY(NOW()) - 20 DAY, '%Y-%m-21') THEN o.total_amount ELSE 0 END) AS overdue_total_amount
FROM Orders o 
NATURAL JOIN Customers c 
RIGHT JOIN Payments p ON o.order_id = p.order_id 
WHERE p.payment_type_id = 2 
GROUP BY o.user_id;
'''

# Get customer overdue orders
GET_CUSTOMER_OVERDUE_ORDERS = '''SELECT * 
FROM Orders 
WHERE user_id = {}
AND order_date < DATE_FORMAT(NOW() - INTERVAL DAY(NOW()) - 20 DAY, '%Y-%m-21');

'''




# GET_RELATED_CATEGORY_PROMO_BY_PRODUCTet products with Category
GET_GIFTCARDS_WITH_CATEGORY = '''SELECT  p.product_id, p.product_name, p.product_description, p.product_price, p.subcategory_id, p.stock_quantity, p.product_image_id, p.oversized, p.product_status, 
s.subcategory_name, s.category_id, c.category_name, Product_Images.product_image
FROM Products p  LEFT JOIN Subcategories s ON p.subcategory_id = s.subcategory_id LEFT JOIN Categories c ON s.category_id = c.category_id LEFT JOIN Product_Images  ON p.product_image_id = Product_Images.product_image_id WHERE p.subcategory_id = 1;'''

# Check Whether PRODUCT BOUGHT BY CUSOMER ID
CHECK_PRODUCT_BOUGHT_BY_CUSTOMER_ID = '''SELECT *  FROM Orders NATURAL JOIN Order_Details WHERE user_id = {} and product_id = {} ;'''



# Check Whether Review Left BY CUSOMER ID
CHECK_REVIEW_LEFT_BY_CUSTOMER_ID = '''SELECT *  FROM Reviews WHERE user_id = {} and product_id = {} ;'''


# Leave new review
LEAVE_NEW_REVIEW = 'INSERT IGNORE INTO Reviews (user_id, product_id, rating_value, review_comment, review_date) VALUES ({}, {},{}, "{}", "{}");'

# Get all reviews with product images
GET_ALL_REVIEWS_WITH_PRODUCT_IMAGES = '''SELECT * FROM Reviews
INNER JOIN Products ON Products.product_id = Reviews.product_id
INNER JOIN Product_Images ON Product_Images.product_image_id = Products.product_image_id;'''

# Hide a review
HIDE_A_REVIEW = 'UPDATE Reviews SET review_status = 0 WHERE product_id = {};'

# Show a review
SHOW_A_REVIEW = 'UPDATE Reviews SET review_status = 1 WHERE product_id = {};'


# Update pending orders with shipping method and total amount
UPDATE_PENDING_ORDERS_WITH_SHIPPING = 'UPDATE Orders  SET shipping_method_id = {}, total_amount = "{}" WHERE order_id = "{}";'

# Select payment detail by order id
GET_PAYMENT_BY_ORDER_ID = '''SELECT *  FROM Payments NATURAL JOIN Payment_Types WHERE order_id = {};'''


# Refund a payment by order id
UPDATE_PAYMENT_STATUS__TO_REFUND_BY_ORDER_ID = 'UPDATE Payments  SET payment_status = 0, payment_type_id = 4 WHERE order_id = "{}";'


# Update accountholder payment to card payment by order id
UPDATE_PAYMENT_STATUS_TO_CARD_PAYMENT_BY_ORDER_ID = 'UPDATE Payments  SET payment_type_id = 1, payment_date_time = "{}" WHERE order_id = "{}";'

# Update accountholder payment to cash/eftpos payment by order id
UPDATE_PAYMENT_STATUS_TO_CASH_PAYMENT_BY_ORDER_ID = 'UPDATE Payments  SET payment_type_id = 1, payment_date_time = "{}" WHERE order_id = "{}";'



# Update payment with giftcard balance
# UPDATE_PAYMENT_WITH_GIFTCARD_BY_ORDER_ID = 'UPDATE Payments  SET payment_amount = {}, gift_card_id = {}, gift_card_amount = {} WHERE order_id = "{}";'


# Get top five highest balance gift card
GET__FIVE_GIFTCARDS_WITH_HIGHEST_BALANCE_BY_ID = '''SELECT *
FROM Gift_Cards
WHERE user_id = {}
  AND gift_card_amount > 0.00
  AND expiry_date >= CURDATE()
ORDER BY gift_card_amount DESC
LIMIT 0, 5; '''

# Select giftcard by card id
GET_GIFTCARD_BY_CARD_ID = '''SELECT *  FROM Gift_Cards  WHERE gift_card_id = {};'''


# update gift card amount by id
UPDATE_GIFT_CARD_AMOUNT_BY_ID = 'UPDATE Gift_Cards SET gift_card_amount = "{}" WHERE gift_card_id = "{}";'

# insert gift card usage history
INSERT_GIFT_CARD_HISTORY = 'INSERT  INTO Giftcard_Payments (payment_id, gift_card_id, payment_amount) VALUES ({}, {}, "{}");'


# Update payment amount if used giftcard
UPDATE_PAYMENT_WITH_GIFT_CARD = 'UPDATE Payments  SET payment_amount = {} WHERE order_id = "{}";'

# Get news
GET_ALL_NEWS = 'SELECT * FROM News ORDER BY news_timestamp DESC;'

# Get news by id
GET_NEWS_BY_ID = 'SELECT * FROM News WHERE news_id = {};'

# Add new news
ADD_NEW_NEWS = 'INSERT INTO News (sender_id, news_subject, news_content, news_image, news_timestamp) VALUES ({}, "{}", "{}", "{}", "{}");'

# Add new news image
INSERT_NEW_NEWS_IMAGE = 'INSERT INTO News (news_image) VALUES ("{}");'

# Update news by id
UPDATE_NEWS_BY_ID = 'UPDATE News SET sender_id = {}, news_subject = "{}", news_content = "{}" WHERE news_id = {};'

# Update news image to null
UPDATE_NEWS_IMAGE_TO_NULL = 'UPDATE News SET news_image = "" WHERE news_id = {};'

# Update news image by id
UPDATE_NEWS_IMAGE_BY_ID = 'UPDATE News SET news_image = "{}" WHERE news_id = {};'

# Delete news by id
DELETE_NEWS_BY_ID = 'DELETE FROM News WHERE news_id = {};'

# Send news by id
SEND_NEWS_BY_ID = 'UPDATE News SET sender_id = {}, news_status = 1 WHERE news_id = {};'

# Register giftcard to one customer
REGISTER_GIFTCARD_TO_ONE_CUSTOMER = 'UPDATE Gift_Cards SET user_id = "{}" WHERE gift_card_id = {};'

# Get order details and product subcategory
GET_PRODUCT_DETAILS_WITH_SUBCATEGORY_BY_ID = 'SELECT * FROM Order_Details NATURAL JOIN Products WHERE order_id = {};'


# Dashaboard queries
PRODUCT_COUNT = 'SELECT count(product_id) FROM Products;'

ACTIVE_PRODUCT_COUNT = 'SELECT count(product_id) FROM Products where product_status = 1;'

INACTIVE_PRODUCT_COUNT = 'SELECT count(product_id) FROM Products where product_status = 0;'


CURRENT_MONTH_ORDERS_COUNT = '''SELECT COUNT(*) AS current_month_orders
                            FROM Orders
                            WHERE YEAR(order_date) = YEAR(CURDATE())
                            AND MONTH(order_date) = MONTH(CURDATE());'''

LAST_MONTH_ORDERS_COUNT = '''SELECT COUNT(*) AS previous_month_orders
                            FROM Orders
                            WHERE YEAR(order_date) = YEAR(CURDATE() - INTERVAL 1 MONTH)
                            AND MONTH(order_date) = MONTH(CURDATE() - INTERVAL 1 MONTH);'''

NEW_MESSAGE_COUNT = 'SELECT count(message_id) FROM Messages where message_status = 1;'

CUSTOMER_COUNT = 'SELECT count(user_id) FROM Customers;'

NEW_APPLICATION_COUNT = '''SELECT COUNT(message_id) AS application_count 
                        FROM Messages 
                        WHERE message_subject = 'Account Holder Application' AND message_status = 1;'''

PRODUCT_SALES_DATA = '''SELECT 
                        p.product_name, 
                        SUM(od.quantity) AS sales 
                        FROM 
                            Products p
                        JOIN 
                            Order_Details od ON p.product_id = od.product_id
                        GROUP BY 
                            p.product_name
                        ORDER BY 
                            sales DESC
                        LIMIT 5;'''

USER_COUNT = 'SELECT count(user_id) FROM Users;'


# Reports

PRODUCTS_REPORT = '''SELECT 
	od.product_id,
    od.product_name,
    SUM(od.quantity) AS total_quantity_sold,
    p.stock_quantity,
    p.product_price
FROM 
    Orders o NATURAL JOIN Order_Details od NATURAL JOIN Products p
WHERE 
    YEAR(order_date) = YEAR(CURRENT_DATE)
    AND MONTH(order_date) = MONTH(CURRENT_DATE)
GROUP BY 
    product_id, product_name
ORDER BY
     total_quantity_sold DESC
LIMIT 0, 20;'''

CUSTOMERS_REPORT = '''SELECT 
	o.user_id,
    SUM(o.total_amount) AS total_spent,
	c.first_name, 
    c.last_name, 
    c.phone, 
    c.points, 
    c.credit_limit
FROM 
    Orders o NATURAL JOIN Customers c
WHERE 
    YEAR(order_date) = YEAR(CURRENT_DATE)
    AND MONTH(order_date) = MONTH(CURRENT_DATE)
GROUP BY 
    user_id
ORDER BY
     total_spent DESC
LIMIT 0, 20;

    
    ;'''

ORDERS_REPORT = '''
SELECT * FROM Orders


WHERE 
    YEAR(order_date) = YEAR(CURRENT_DATE)
    AND MONTH(order_date) = MONTH(CURRENT_DATE)

ORDER BY
     total_amount DESC
LIMIT 0, 20;

;

'''



PRODUCTS_REPORT_GIVEN_DATE = '''
SELECT 
    od.product_id,
    od.product_name,
    SUM(od.quantity) AS total_quantity_sold,
    p.stock_quantity,
    p.product_price
FROM 
    Orders o
    NATURAL JOIN Order_Details od
    NATURAL JOIN Products p
WHERE 
    order_date BETWEEN '{}' AND '{}'
GROUP BY 
    product_id, product_name
ORDER BY
    total_quantity_sold DESC
LIMIT 0, 20;

'''

CUSTOMERS_REPORT_GIVEN_DATE = '''
SELECT 
    o.user_id,
    SUM(o.total_amount) AS total_spent,
    c.first_name, 
    c.last_name, 
    c.phone, 
    c.points, 
    c.credit_limit
FROM 
    Orders o
    NATURAL JOIN Customers c
WHERE 
    order_date BETWEEN '{}' AND '{}'
GROUP BY 
    user_id
ORDER BY
    total_spent DESC
LIMIT 0, 20;


'''

ORDERS_REPORT_GIVEN_DATE = '''
SELECT * FROM Orders
WHERE 
    order_date BETWEEN '{}' AND '{}'
ORDER BY
    total_amount DESC
LIMIT 0, 20;


'''

# Promotion Products to Verify
GET_ALL_PROMOTION_PRODUCTS_TO_VERIFY = 'SELECT * FROM Promotion_Products NATURAL JOIN Promotions WHERE Promotions.status = "Active";'

GET_ALL_PROMOTION_SUBCATOGERIES_TO_VERIFY = 'SELECT * FROM Promotion_Subcategories NATURAL JOIN Promotions WHERE Promotions.status = "Active"; '

GET_ALL_PROMOTION_CATOGERIES_TO_VERIFY = 'SELECT * FROM Promotion_Categories NATURAL JOIN Subcategories NATURAL JOIN Promotions WHERE Promotions.status = "Active";'



# Get all orders
GET_ALL_ORDERS_BY_CUSTOMER_ID = '''SELECT 
    o.order_id, 
    o.user_id, 
    o.order_date, 
    o.total_amount, 
    o.shipping_method_id, 
    o.order_status, 
    o.shipping_address,      
    sm.shipping_method_id, 
    sm.shipping_name, 
    sm.shipping_price 
FROM Orders o 
LEFT JOIN Shipping_Methods sm ON o.shipping_method_id = sm.shipping_method_id
WHERE  o.user_id = "{}"
ORDER BY
    CASE order_status
        WHEN 'paid' THEN 1
        WHEN 'pending' THEN 2
        WHEN 'preparing' THEN 3
        WHEN 'ready' THEN 4
        WHEN 'sent' THEN 5
        WHEN 'placed' THEN 6
        WHEN 'finished' THEN 7
        WHEN 'cancelled' THEN 8
        ELSE 9 
    END
    ;

'''