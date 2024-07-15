-- Remove this line if you dont want to initialize your database
-- DROP SCHEMA IF  EXISTS Moa;

-- CREATE SCHEMA IF NOT EXISTS Moa;
-- USE Moa;

DROP TABLE IF EXISTS User_Gift_Card_Records;
DROP TABLE IF EXISTS  Giftcard_Payments;
DROP TABLE IF EXISTS Gift_Cards;
DROP TABLE IF EXISTS User_Gift_Card_Points_Level;
DROP TABLE IF EXISTS News;
DROP TABLE IF EXISTS Message_Contents;
DROP TABLE IF EXISTS Messages;
DROP TABLE IF EXISTS Promotion_Products;
DROP TABLE IF EXISTS Promotion_Categories;
DROP TABLE IF EXISTS Promotion_Subcategories;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Shopping_Carts;
DROP TABLE IF EXISTS User_Payment_Cards;

DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Order_Details;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Addresses;
DROP TABLE IF EXISTS Admins;
DROP TABLE IF EXISTS Staff;
DROP TABLE IF EXISTS Managers;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Product_Images;
DROP TABLE IF EXISTS Products;


DROP TABLE IF EXISTS Subcategories;


DROP TABLE IF EXISTS Categories;


DROP TABLE IF EXISTS Payment_Types;


DROP TABLE IF EXISTS Shipping_Methods;

DROP TABLE IF EXISTS Promotions;






-- User Tables
CREATE TABLE Users (
user_id INT AUTO_INCREMENT PRIMARY KEY,
email_address VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
salt VARCHAR(255) NOT NULL,
user_type ENUM("customer", "staff", "manager","admin") DEFAULT "customer" NOT NULL,
user_status TINYINT DEFAULT 1
);

INSERT INTO Users (email_address, password, salt, user_type)
VALUES ('simon123@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'staff'),
		('simon456@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'staff'),
       ('mark123@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'manager'),
          ('tim123@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'admin');
         
  


ALTER TABLE Users AUTO_INCREMENT = 10000;





CREATE TABLE Addresses (
address_id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
unit_number VARCHAR(20),
address_line1 VARCHAR(500),
address_line2 VARCHAR(500),
city VARCHAR(200),
region ENUM("Northland", "Auckland", "Waikato", "Bay-of-Plenty", "Gisborne", "Hawkes-Bay", "Taranaki", "Manawatu-Wanganui", "Wellington", "Tasman", "Nelson", "Marlborough", "West-Coast", "Canterbury", "Otago", "Southland", "Outer-Islands"),
postcode CHAR(4),
CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON UPDATE CASCADE

);

CREATE TABLE Customers (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    register_date DATE,
    phone VARCHAR(20),
    profile_image VARCHAR(255) default "default-image.jpg",
    points INT DEFAULT 0 NOT NULL,
    credit_limit DECIMAL(10,2),
    address_id INT ,
	CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON UPDATE CASCADE,
    CONSTRAINT FOREIGN KEY (address_id) REFERENCES Addresses(address_id) ON UPDATE CASCADE ON DELETE SET NULL
  
);


CREATE TABLE Staff (
user_id INT PRIMARY KEY,
first_name VARCHAR(50),
last_name VARCHAR(50),
profile_image VARCHAR(255) default "default-image.jpg",
phone VARCHAR(20),
CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON UPDATE CASCADE
);

INSERT INTO Staff (user_id, first_name, last_name)
VALUES 
       ('1', 'Simon', 'Zhang'),
       ('2', 'Simonie', 'Alex');

CREATE TABLE Managers (
user_id INT PRIMARY KEY,
first_name VARCHAR(50),
last_name VARCHAR(50),
profile_image VARCHAR(255) default "default-image.jpg",
phone VARCHAR(20),
CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON UPDATE CASCADE
);

INSERT INTO Managers (user_id, first_name, last_name)
VALUES 
		('3', 'Mark', 'Rick');
     



CREATE TABLE Admins (
user_id INT PRIMARY KEY,
first_name VARCHAR(50),
last_name VARCHAR(50),
profile_image VARCHAR(255) default "default-image.jpg",
phone VARCHAR(20),
CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON UPDATE CASCADE
);

INSERT INTO Admins (user_id, first_name, last_name)
VALUES 
		('4', 'Tim', 'Plas');
  


-- Product Tables
CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100)
);

INSERT INTO Categories (category_name) VALUES 
('Gift Card');


ALTER TABLE Categories AUTO_INCREMENT = 10;

CREATE TABLE Subcategories (
    subcategory_id INT AUTO_INCREMENT PRIMARY KEY,
    subcategory_name VARCHAR(100),
    category_id INT,
    CONSTRAINT FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON UPDATE CASCADE
);


INSERT INTO Subcategories (subcategory_name, category_id) VALUES
('Gift Card',1);

ALTER TABLE Subcategories AUTO_INCREMENT = 100;


-- oversized: 0 for standard product, 1 for oversize item, 2 for big item, must pick-up
CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    product_description TEXT,
    product_price DECIMAL(10,2) NOT NULL,
    subcategory_id INT,
    stock_quantity INT DEFAULT 0,
    product_image_id INT DEFAULT 0,
    oversized TINYINT DEFAULT 0,
    product_status TINYINT DEFAULT 1
);

INSERT INTO Products (product_name, product_description, product_price, subcategory_id, stock_quantity, product_image_id, oversized, product_status) VALUES 
('Gift Card $20', 'Gift Card $20. Please register first before use.', 20.00, 1, 9999, 16, 0, 1),
('Gift Card $50', 'Gift Card $50. Please register first before use.', 50.00, 1, 9999, 17, 0, 0),
('Gift Card $100', 'Gift Card $100. Please register first before use.', 100.00, 1, 9999, 18, 0, 1),
('Gift Card TEST', 'Gift Card Test1', 9999.00, 1, 9999, 0, 0, 0),
('Gift Card TEST', 'Gift Card Test2', 9999.00, 1, 9999, 0, 0, 0);




ALTER TABLE Products AUTO_INCREMENT = 10000;

CREATE TABLE Product_Images (
    product_image_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    INDEX `product_id_idx` (`product_id` ASC) VISIBLE,
    product_image VARCHAR(255) NOT NULL
);



ALTER TABLE Products
ADD CONSTRAINT fk_subcategory
FOREIGN KEY (subcategory_id) REFERENCES Subcategories(subcategory_id) ON UPDATE CASCADE;

ALTER TABLE Product_Images
ADD CONSTRAINT fk_product
FOREIGN KEY (product_id) REFERENCES Products(product_id) ON UPDATE CASCADE;


-- Shopping Cart Tables
CREATE TABLE Shopping_Carts (
user_id INT,
product_id INT,
qty INT,
PRIMARY KEY (`user_id`, `product_id`),
CONSTRAINT FOREIGN KEY (user_id) REFERENCES Customers(user_id) ON UPDATE CASCADE ,
CONSTRAINT FOREIGN KEY (product_id) REFERENCES Products(product_id)    ON UPDATE CASCADE 
);


-- Payment Tables
CREATE TABLE Payment_Types (
payment_type_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
payment_type_name VARCHAR(100)

);

INSERT INTO Payment_Types (payment_type_name)
VALUES 
        ('Debit Card/Credit Card/Giftcard'),
        ('Account Balance'),
        ('Cash/Eftpos'),
        ('Refund');
  

CREATE TABLE Gift_Cards (
    gift_card_id INT  AUTO_INCREMENT PRIMARY KEY,
    gift_card_number VARCHAR(20),
    gift_card_amount DECIMAL(10,2),
    user_id INT,
    INDEX `giftcard_user_id_idx` (`user_id` ASC) VISIBLE,
    source ENUM("buy", "reward", "refund","gift") DEFAULT "buy",
    expiry_date DATE,
    CONSTRAINT FOREIGN KEY (user_id) REFERENCES Customers(user_id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    user_id INT NOT NULL,
    INDEX `payment_user_id_idx` (`user_id` ASC) VISIBLE,
    order_id INT NOT NULL,
    INDEX `payment_order_id_idx` (`order_id` ASC) VISIBLE,
    payment_date_time DATETIME NOT NULL,
    payment_amount DECIMAL(8,2) NOT NULL,
    payment_type_id INT NOT NULL,
	payment_status TINYINT DEFAULT 1,
    CONSTRAINT FOREIGN KEY (user_id) REFERENCES Customers(user_id) ON UPDATE CASCADE ,
    CONSTRAINT FOREIGN KEY (payment_type_id) REFERENCES Payment_Types(payment_type_id) ON UPDATE CASCADE 
);

CREATE TABLE IF NOT EXISTS Giftcard_Payments (
    payment_id INT,
    gift_card_id INT,
	payment_amount DECIMAL(8,2) NOT NULL,
    PRIMARY KEY (`payment_id`, `gift_card_id`),
    CONSTRAINT FOREIGN KEY (payment_id) REFERENCES Payments(payment_id) ON UPDATE CASCADE ,
    CONSTRAINT FOREIGN KEY (gift_card_id) REFERENCES Gift_Cards(gift_card_id) ON UPDATE CASCADE 
);


-- Order Tables
CREATE TABLE Shipping_Methods (

shipping_method_id INT AUTO_INCREMENT PRIMARY KEY,
shipping_name VARCHAR(100),
shipping_price FLOAT(12, 2)
);

INSERT INTO Shipping_Methods (shipping_name, shipping_price)
VALUES 
		('Flat', '10'),
       ('Oversized', '100'),
       ('Pick-up', '0'),
       ('Custom1', '13.66');

ALTER TABLE Shipping_Methods AUTO_INCREMENT = 100;


-- order_status: order placed, order being prepared by staff, order pending for freight price, order paid, sent for delivery, ready for pickup, finished, cancelled
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    INDEX `user_order_id_idx` (`user_id` ASC) VISIBLE,
    order_date DATE,
    total_amount DECIMAL(10,2),
    shipping_method_id INT,
	order_status ENUM("placed", "preparing", "pending","paid", "sent","ready","finished","cancelled") DEFAULT "placed",
    
    INDEX `order_status_idx` (`order_status` ASC) VISIBLE,
    processor_id INT,
    shipping_address VARCHAR(255),
  
    CONSTRAINT FOREIGN KEY (user_id) REFERENCES Customers(user_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT FOREIGN KEY (processor_id) REFERENCES Users(user_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT FOREIGN KEY (shipping_method_id) REFERENCES Shipping_Methods(shipping_method_id) ON UPDATE CASCADE ON DELETE SET NULL
   
    
);

ALTER TABLE Payments
ADD CONSTRAINT fk_order_id
FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON UPDATE CASCADE ;



CREATE TABLE Order_Details (
    order_id INT,
    product_id INT,
    product_name VARCHAR(100),
    quantity INT,
    unit_price DECIMAL(10,2),
	discount_rate DECIMAL(3,2) DEFAULT 0,
    final_unit_price DECIMAL(10,2),
    PRIMARY KEY (`order_id`, `product_id`),
    CONSTRAINT FOREIGN KEY (order_id) REFERENCES Orders(order_id)     ON UPDATE CASCADE ,
    CONSTRAINT FOREIGN KEY (product_id) REFERENCES Products(product_id)     ON UPDATE CASCADE 
);





-- Promotion Tables
CREATE TABLE Promotions (
promotion_id INT AUTO_INCREMENT PRIMARY KEY,
promotion_name VARCHAR(200),
promotion_description VARCHAR(2000),
promotion_type ENUM("product", "subcategory","category") ,
discount_rate DECIMAL(3,2) DEFAULT 0,
special_condition VARCHAR(200),
promotion_image VARCHAR(255) default "default-promotion-image.jpg",
status ENUM("Active", "Inactive", "Coming Soon", "Deleted", "Expired"),
start_date DATETIME,
end_date DATETIME
);

CREATE TABLE Promotion_Products (
promotion_id INT,
product_id INT,
PRIMARY KEY (`promotion_id`, `product_id`),
    CONSTRAINT FOREIGN KEY (promotion_id) REFERENCES Promotions(promotion_id) ON UPDATE CASCADE ,
    CONSTRAINT FOREIGN KEY (product_id) REFERENCES Products(product_id)  ON UPDATE CASCADE 
);

CREATE TABLE Promotion_Categories (
promotion_id INT,
category_id INT,

PRIMARY KEY (`promotion_id`, `category_id`),
CONSTRAINT FOREIGN KEY (promotion_id) REFERENCES Promotions(promotion_id)     ON UPDATE CASCADE ,
    CONSTRAINT FOREIGN KEY (category_id) REFERENCES Categories(category_id)     ON UPDATE CASCADE 
);


CREATE TABLE Promotion_Subcategories (
promotion_id INT,
subcategory_id INT,

PRIMARY KEY (`promotion_id`, `subcategory_id`),
    CONSTRAINT FOREIGN KEY (promotion_id) REFERENCES Promotions(promotion_id)     ON UPDATE CASCADE ,
    CONSTRAINT FOREIGN KEY (subcategory_id) REFERENCES Subcategories(subcategory_id)    ON UPDATE CASCADE
);





-- Additional Tables
CREATE TABLE Reviews (
user_id INT,
product_id INT,
rating_value INT DEFAULT 5,
review_comment VARCHAR(2000),
review_status TINYINT DEFAULT 1,
review_date DATE,
PRIMARY KEY (`user_id`, `product_id`),
CONSTRAINT FOREIGN KEY (user_id) REFERENCES Customers(user_id) ON UPDATE CASCADE ,
CONSTRAINT FOREIGN KEY (product_id) REFERENCES Products(product_id)    ON UPDATE CASCADE 
);




CREATE TABLE User_Gift_Card_Points_Level (
  level_id	INT  AUTO_INCREMENT PRIMARY KEY,
  level_point INT  NOT NULL,
  gift_card_amount INT  NOT NULL
);

INSERT INTO User_Gift_Card_Points_Level (level_point, gift_card_amount)
VALUES 
       ('1000','20'),
       ('2000','50'),
       ('3000','80');
  


CREATE TABLE User_Gift_Card_Records (
  user_id INT ,
  gift_card_id INT,
  level_point INT,
  record_date DATE,
  PRIMARY KEY (`user_id`, `gift_card_id`),

	CONSTRAINT FOREIGN KEY (user_id) REFERENCES Customers(user_id) ON UPDATE CASCADE ,
	CONSTRAINT FOREIGN KEY (gift_card_id) REFERENCES Gift_Cards(gift_card_id) ON UPDATE CASCADE 
);


CREATE TABLE News (
    news_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT DEFAULT 0,
    news_subject VARCHAR(255),
    news_content TEXT,
    news_image VARCHAR(255),
	news_timestamp DATETIME,
    news_status TINYINT DEFAULT 0,
    CONSTRAINT FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON UPDATE CASCADE
);

CREATE EVENT IF NOT EXISTS update_news_status
ON SCHEDULE EVERY 7 DAY
STARTS CONCAT(CURDATE(), ' 00:00:00')
DO
  UPDATE News
  SET news_status = 0
  WHERE news_timestamp <= DATE_SUB(CURDATE(), INTERVAL 30 DAY) AND news_status != 0;

CREATE TABLE Messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    INDEX `message_user_id_idx` (`user_id` ASC) VISIBLE,
    message_subject VARCHAR(255),
    message_status TINYINT DEFAULT 1,
    CONSTRAINT FOREIGN KEY (user_id) REFERENCES Users(user_id) ON UPDATE CASCADE
);

CREATE TABLE Message_Contents (
    message_content_id INT AUTO_INCREMENT  PRIMARY KEY, 
	message_id INT,
	INDEX `message_id_idx` (`message_id` ASC) VISIBLE,
    message_content TEXT,
    message_timestamp DATETIME,
	responder_id TINYINT DEFAULT 0,
    CONSTRAINT FOREIGN KEY (message_id) REFERENCES Messages(message_id) ON UPDATE CASCADE
);



INSERT INTO Users (email_address, password, salt, user_type) VALUES 
('john.doe@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('jane.smith@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('mike.brown@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('amy.wilson@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('chris.evans@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('lisa.johnson@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('david.wong@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('sarah.nguyen@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('kevin.lee@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('emily.chen@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer');


INSERT INTO Addresses (user_id, unit_number, address_line1, address_line2, city, region, postcode) VALUES 
(10000, 'Suite 1001', '789 Oak Lane', '', 'Hometown', 'Southland', '1234'),
(10000, '', '456 Pine Street', '', 'Village', 'Auckland', '5678'),
(10001, 'Apt 505', '321 Elm Avenue', '', 'City Center', 'Manawatu-Wanganui', '9012'),
(10001, '', '789 Maple Road', '', 'Riverside', 'Wellington', '3456'),
(10002, 'Unit 10', '101 Cedar Street', '', 'Lakeside', 'Gisborne', '7890'),
(10003, 'Apt 202', '222 Birch Lane', '', 'Hilltop', 'Auckland', '2345'),
(10004, '', '333 Spruce Avenue', '', 'Seaside', 'Northland', '6789'),
(10005, 'Suite 500', '444 Holly Street', '', 'Mountainside', 'Taranaki', '0123'),
(10005, '', '555 Walnut Road', '', 'Valley', 'Canterbury', '4567'),
(10006, 'Unit 3', '666 Fir Lane', '', 'Highland', 'Canterbury', '8901'),
(10007, 'Apt 101', '777 Beech Avenue', '', 'Lowland', 'Canterbury', '2345'),
(10008, '', '888 Sycamore Street', '', 'Woodland', 'Canterbury', '6789'),
(10008, 'Suite 200', '999 Poplar Road', '', 'Meadow', 'Southland', '0123'),
(10008, '', '111 Ash Lane', '', 'Prairie', 'Southland', '4567'),
(10008, 'Unit 5', '222 Juniper Avenue', '', 'Garden', 'Southland', '8901');



INSERT INTO Customers (user_id, first_name, last_name, phone, address_id, points, credit_limit, register_date) VALUES 
(10000, 'John', 'Doe', '02134567890', 2, 3800, 1000.00, '2023-06-01'),
(10001, 'Jane', 'Smith', '02276543210', 3, 500, 0, '2022-06-01'),
(10002, 'Mike', 'Brown', '027555444333', 5, 1000, 0, '2024-02-01'),
(10003, 'Amy', 'Wilson', '021112223333', 6, 1300, 0, '2024-03-01'),
(10004, 'Chris', 'Evans', '022999888777', 7, 0, 0, '2024-01-01'),
(10005, 'Lisa', 'Johnson', '021777666555', 9, 100, 3000.00, '2022-06-01'),
(10006, 'David', 'Wong', '027444555666', 10, 0, 0, '2023-06-01'),
(10007, 'Sarah', 'Nguyen', '021333222111', 11, 0, 0, '2024-05-01'),
(10008, 'Kevin', 'Lee', '022222333444', 14, 0, 900.00, '2023-06-01'),
(10009, 'Emily', 'Chen', '021666777888', Null, 0, 0, '2023-06-01');

INSERT INTO Categories (category_name) VALUES 
('Animal Health Care'),
('Animal Feed and Nutrition'),
('Dairy Hygiene and Supplies'),
('Calving Supplies'),
('Animal Equipment'),
('Water Management'),
('Fencing and Barriers'),
('Work Clothing'),
('Footwear'),
('Household Supplies'),
('Garden Supplies'),
('Agrichemicals'),
('Machinery and Oil'),
('Pasture and Cropping'),
('Fertilizers');



INSERT INTO Subcategories (subcategory_name, category_id) VALUES 
-- Animal Health Care
('Veterinary Medicines', 10),
('Animal Supplements', 10),
('Animal First Aid', 10),

-- Animal Feed and Nutrition
('Animal Feed', 11),
('Mineral Blocks', 11),

-- Dairy Hygiene and Supplies
('Milking Equipment', 12),
('Dairy Cleaners', 12),
('Teat Sprays', 12),

-- Calving Supplies
('Calving Equipment', 13),
('Calf Milk Replacers', 13),
('Calf Feeders', 13),

-- Animal Equipment
('Livestock Handling Equipment', 14),
('Grooming Tools', 14),
('Tagging Equipment', 14),

-- Water Management
('Water Tanks', 15),
('Irrigation Systems', 15),
('Water Pumps', 15),

-- Fencing and Barriers
('Fencing Supplies', 16),
('Electric Fencing', 16),
('Gates and Panels', 16),

-- Work Clothing
('Workwear', 17),
('Protective Gear', 17),
('Hi-Vis Clothing', 17),

-- Footwear
('Boots', 18),
('Work Shoes', 18),
('Wellington Boots', 18),

-- Household Supplies
('Cleaning Supplies', 19),
('Storage Solutions', 19),
('Household Tools', 19),

-- Garden Supplies
('Gardening Tools', 20),
('Plant Seeds', 20),
('Garden Fertilizers', 20),

-- Agrichemicals
('Herbicides', 21),
('Pesticides', 21),
('Fungicides', 21),

-- Machinery and Oil
('Farm Machinery', 22),
('Machine Oil', 22),
('Spare Parts', 22),

-- Pasture and Cropping
('Seeds', 23),
('Crop Protection', 23),
('Soil Conditioners', 23),

-- Fertilizers
('Fertilizer Types', 24),
('Organic Fertilizers', 24),
('Liquid Fertilizers', 24);



INSERT INTO Products (product_name, product_description, product_price, subcategory_id, stock_quantity, product_image_id, oversized, product_status) VALUES 
('Antibiotics for Livestock', 'A highly effective medication designed to treat a range of bacterial infections in livestock, ensuring their health and productivity are maintained. Suitable for cattle, sheep, pigs, and goats.', 29.99, 100, 50, 1, 0, 1),
('Mineral Supplements for Cattle', 'These supplements provide essential minerals that enhance cattle health, boost immunity, and improve overall productivity. Perfect for dairy and beef cattle.', 39.99, 103, 30, 2, 0, 1),
('Milking Machine', 'An advanced automatic milking machine that streamlines the milking process, reducing labor and increasing efficiency. Ideal for medium to large dairy farms.', 4999.99, 105, 20, 3, 2, 1),
('Calving Pen', 'A robust and secure calving pen designed to ensure the safety of both the cow and calf during the calving process. Made from high-quality materials.', 999.99, 108, 10, 4, 1, 1),
('Cattle Crush', 'A heavy-duty cattle crush that provides safe and efficient handling of livestock. Essential for veterinary treatments and routine inspections.', 1999.99, 111, 15, 5, 2, 1),
('Water Storage Tank', 'A large capacity water storage tank suitable for agricultural use. Made from durable materials to withstand harsh weather conditions.', 799.99, 114, 5, 6, 2, 1),
('Barbed Wire', 'High-quality barbed wire ideal for creating secure fencing for livestock. Durable and resistant to weathering, ensuring long-lasting protection.', 19.99, 117, 100, 7, 0, 1),
('Farm Overalls', 'Durable and comfortable overalls designed for farm work. Made from high-quality materials, they provide protection and ease of movement.', 49.99, 120, 80, 8, 0, 1),
('Steel Toe Boots', 'Safety boots featuring a steel toe cap for maximum protection during farm work. Waterproof and slip-resistant, ideal for all weather conditions.', 100.00, 123, 60, 9, 0, 1),
('Cleaning Detergent', 'A powerful detergent specially formulated for cleaning farm equipment. Removes tough dirt and grime, ensuring hygiene and safety.', 14.99, 126, 200, 10, 0, 1),
('Garden Hose', 'A heavy-duty garden hose designed for efficient watering. Made from durable materials to prevent kinking and ensure a steady water flow.', 29.99, 129, 150, 11, 0, 1),
('Herbicide Spray', 'A selective herbicide spray that effectively controls weeds without harming crops. Easy to apply and provides long-lasting protection.', 39.99, 132, 50, 12, 0, 1),
('Tractor', 'A powerful tractor equipped with advanced features for various farm operations. Ensures efficiency and productivity in large-scale farming.', 49999.99, 135, 5, 13, 2, 1),
('Grass Seeds', 'High-quality grass seeds that promote pasture improvement. Fast germinating and drought-resistant, ideal for various soil types.', 9.99, 138, 100, 14, 0, 1),
('NPK Fertilizer', 'A complete NPK fertilizer that provides essential nutrients for crop growth. Enhances soil fertility and improves crop yield.', 49.99, 141, 30, 15, 0, 1),
('Drench for Sheep', 'An oral drench that effectively controls internal parasites in sheep. Improves health and weight gain, essential for productive farming.', 45.99, 101, 40, 19, 0, 1),
('Vitamin Supplements for Pigs', 'Essential vitamin supplements that improve pig health and growth. Boosts immunity and ensures overall well-being of pigs.', 34.99, 101, 25, 20, 0, 1),
('Portable Calving Aid', 'A portable aid designed to assist in difficult calvings. Easy to use and transport, ensuring safe delivery of calves.', 499.99, 102, 7, 21, 0, 1),
('Sheep Shearing Machine', 'A high-efficiency shearing machine designed for sheep. Provides quick and smooth shearing, reducing stress on animals.', 749.99, 112, 18, 22, 0, 1),
('Electric Fence Energizer', 'An energizer for electric fencing systems that ensures reliable power supply. Keeps livestock contained and predators out.', 199.99, 118, 50, 23, 0, 1),
('Thermal Work Jacket', 'An insulated jacket designed for cold weather farm work. Provides warmth and comfort, made from durable and breathable materials.', 100.99, 120, 45, 24, 0, 1),
('Waterproof Farm Boots', 'Waterproof boots designed for wet and muddy conditions. Provide comfort and protection, essential for farm work.', 79.99, 123, 55, 25, 0, 1),
('Multi-purpose Cleaner', 'An all-purpose cleaner suitable for various surfaces on the farm. Effective in removing dirt, grease, and stains.', 12.99, 126, 180, 26, 0, 1),
('Pruning Shears', 'High-quality pruning shears ideal for garden maintenance. Sharp and durable, ensuring clean cuts and easy handling.', 19.99, 129, 130, 27, 0, 1),
('Organic Weedkiller', 'A natural weedkiller perfect for organic farming. Effectively controls weeds without harming the environment.', 29.99, 132, 40, 28, 0, 1),
('Clover Seeds', 'Premium clover seeds that enrich pastures. Fast-growing and nutritious, improving soil fertility and livestock feed quality.', 14.99, 138, 90, 29, 0, 1),
('Organic Fertilizer', 'Organic fertilizer that promotes sustainable farming. Enhances soil health and fertility, suitable for various crops.', 39.99, 142, 35, 30, 0, 1);



-- Sample test data for Promotions table
INSERT INTO Promotions (promotion_name, promotion_description, promotion_type, discount_rate, start_date, end_date, promotion_image, status) VALUES 
('Everyday Low Price', 'Everyday great deals!', 'product', 0.2, '2020-01-01', '2099-12-31','Everyday_Sale.png', "Active"),
('Winter Sale', 'Big discounts on selected products for the summer season', 'product', 0.2, '2024-06-01', '2024-08-31','Winter_Sale.png', "Active"),
('July Sale', 'Special offers this July', 'subcategory', 0.15, '2024-07-01', '2024-09-30', 'Back_to_School.png', "Inactive"),
('Spring Clearance', 'Clearance sale on various farm equipment', 'category', 0.3, '2024-03-15', '2024-05-30', 'Spring_Clearance.jpeg', "Active"),
('May Sale', 'Savings on workwear, cleaning supplies and gardening tools', 'subcategory', 0.2, '2024-05-01', '2024-05-31', 'May_Sale.jpg', "Active");
-- Buy one get one free promotion
INSERT INTO Promotions (promotion_name, promotion_description, promotion_type, discount_rate, special_condition, promotion_image, status, start_date, end_date) VALUES 
("Buy One Get One FREE!", "Get a free item when you buy one!", "product", 0, "buyOneGetOneFree", "buy-one-get-free-promotion-600nw-2328077451.jpg", "Active", "2024-06-01 00:00:00", "2025-06-01 00:00:00");

INSERT INTO Promotion_Subcategories (promotion_id, subcategory_id) VALUES 
(4, 108);

INSERT INTO Promotion_Categories (promotion_id, category_id) VALUES 
(3, 14);

INSERT INTO Promotion_Products (promotion_id, product_id) VALUES 
(1, 10000),
(1, 10008),
(6, 10026),
(6, 10002);



INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status, processor_id, shipping_address) VALUES 
(10005, '2024-04-03', 100.00, 3, 'finished', 1, '123 Main St, Cityville, Region X, 1234');


INSERT INTO Payments (user_id,order_id, payment_amount, payment_date_time, payment_type_id) VALUES 
(10005, LAST_INSERT_ID(),  100.00, '2024-04-13 18:00:00', 2);


INSERT INTO Order_Details (order_id, product_id, product_name,  quantity, unit_price, final_unit_price) VALUES 
(LAST_INSERT_ID(), 10008, 'Steel Toe Boots', 1, 100.00, 100.00);

INSERT INTO Product_Images (product_id, product_image) VALUES 
(10000, 'Antibiotics for Livestock.jpg'),
(10001, 'Mineral Supplements for Cattle.jpg'),
(10002, 'Milking Machine.jpg'),
(10003, 'Calving Pen.jpg'),
(10004, 'Cattle Crush.jpg'),
(10005, 'Water Storage Tank.jpg'),
(10006, 'Barbed Wire.jpg'),
(10007, 'Farm Overalls.jpg'),
(10008, 'Steel Toe Boots.jpg'),
(10009, 'Cleaning Detergent.jpg'),
(10010, 'Garden Hose.jpg'),
(10011, 'Herbicide Spray.jpg'),
(10012, 'Tractor.png'),
(10013, 'Grass Seeds.jpg'),
(10014, 'NPK Fertilizer.jpeg'),
(1, 'Golden-Gift-Card.jpg'),
(2, 'Golden-Gift-Card copy.jpg'),
(3, 'Golden-Gift-Card copy 2.jpg'),
(10015, 'Drench for Sheep.jpg'),
(10016, 'Vitamin Supplements for Pigs.jpg'),
(10017, 'Portable Calving Aid.jpg'),
(10018, 'Sheep Shearing Machine.jpg'),
(10019, 'Electric Fence Energizer.jpg'),
(10020, 'Thermal Work Jacket.jpg'),
(10021, 'Waterproof Farm Boots.jpg'),
(10022, 'Multi-purpose Cleaner.jpg'),
(10023, 'Pruning Shears.jpg'),
(10024, 'Organic Weedkiller.jpg'),
(10025, 'Clover Seeds.jpg'),
(10026, 'Organic Fertilizer.jpg'),
(10008, 'Steel Toe Boots1.jpg'),
(10008, 'Steel Toe Boots2.jpg');



INSERT INTO Messages (user_id, message_subject, message_status) VALUES 
(10000,'Account Holder Application', 0),
(10000,'Re: Account Holder Application', 1),
(10003,'General Enquiries', 1),
(10005,'The brand of the overall?', 1),
(10007,'Order question', 1),
(10008,'Shipping by freight', 1),
(10009,'Issue with item i recevied', 1),
(10002,'Account Holder Application', 1),
(10000,'Can you top up more items of this product?', 0),
(10000,'Re: Can you top up more items of this product?', 1);


INSERT INTO Message_Contents (message_id, message_content, message_timestamp, responder_id) VALUES 
(1, "Legal Name: John Doe, 
Email: john.doe@example.com,
Address: Suite 1001, 789 Oak Lane, Hometown, Region A, 1234,
Monthly Limit applied: 1000
", '2024-04-13 13:00:00', 0),
(2, "Congratulations, your application has been approved!", '2024-04-13 18:00:00', 3),
(3, "I have a general enguiry, will you add more of your products in the future?", '2024-04-16 14:36:00', 0),
(4, "Hi team, I want to know what is the brand of the overall? Is the quality good?", '2024-04-18 19:10:00', 0),
(5, "Hi, How long will it take to receive my orders generally?", '2024-04-18 21:10:00', 0),
(6, "hey there, i live in rural area, can i arrange shipping by a freight provider?", '2024-04-19 21:40:00', 0),
(7, "I cannot believe my item is broken, how do you deal with this situation?", '2024-04-20 9:22:00', 0),
(8, "Legal Name: Mike Brown, 
Email: mike.brown@example.com,
Address: Unit 10, 101 Cedar Street, Lakeside, Region E, 7890,
Monthly Limit applied: 3000
", '2024-05-13 12:00:00', 0),
(9, "Good morning, I want to order this product but it's out of stock. Can you add more items for me please?", '2024-04-20 9:22:00', 0),
(10, "Dear John, the items have been added in our stock. Please let us know if any more questions. Happy shopping!", '2024-04-21 8:31:00', 2);

INSERT INTO Reviews (user_id, product_id, rating_value, review_comment, review_date) VALUES 
(10000,10008, 5, 'Great product!',  '2024-04-08'),
(10001,10003, 4, 'I like the quality, but is slightly smaller than i expected.',  '2024-04-2'),
(10002,10002, 5, 'This machine helps increasing the productivity a lot!',  '2024-05-2'),
(10003,10007, 4, 'Style is ok, quality is average',  '2024-04-21'),
(10004,10005, 5, 'Good as expected, i placed it and worked well',  '2024-04-28'),
(10005,10006, 3, 'it is rusted!',  '2024-03-23'),
(10006,10009, 5, 'My cleaning went well!',  '2024-05-2'),
(10007,10012, 5, 'I love my new big guy, it rocks!',  '2024-04-8'),
(10008,10013, 3, 'it grows relatively slow, it is fine~',  '2024-03-19'),
(10009,10000, 5, 'My livestocks were sick, this helps a lot!',  '2024-05-11');


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status, processor_id, shipping_address) VALUES 
(10006, '2024-04-03', 100.00, 3, 'finished', 1, '123 Main St, Cityville, Region X, 1234');


INSERT INTO Payments (user_id,order_id, payment_amount, payment_date_time, payment_type_id) VALUES 
(10005, LAST_INSERT_ID(),  100.00, '2024-04-13 18:00:00', 3);


INSERT INTO Order_Details (order_id, product_id, product_name,  quantity, unit_price, final_unit_price) VALUES 
(LAST_INSERT_ID(), 10008, 'Steel Toe Boots', 1, 100.00, 100.00);



-- more test data


INSERT INTO Users (email_address, password, salt, user_type) VALUES 
('mark.thompson@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('laura.white@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('ryan.garcia@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('olivia.martinez@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('jacob.robinson@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('ava.clark@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('nathan.hall@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('mia.thomas@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('ethan.lopez@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('ava.hernandez@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('mason.mitchell@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('emma.perez@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('noah.gonzalez@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('isabella.roberts@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('oliver.hill@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('sophia.howard@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('jackson.ramirez@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('amelia.yang@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('aiden.gomez@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('mia.kelly@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('lucas.bailey@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('harper.russell@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('daniel.kim@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('evelyn.fernandez@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('logan.walker@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('ella.cook@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('carter.morris@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('avery.nguyen@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer'),
('jack.gonzales@example.com', '8a1dbd9783748dc1f858397a0838cf6f8dcf201cccc7e1d94f1a0f287c6601fb', '7c91368c334a4ef898ec245fbaa5e1fb', 'customer');



INSERT INTO Addresses (user_id, unit_number, address_line1, address_line2, city, region, postcode) VALUES 

(10010, 'Suite 1001', '123 Oak Lane', '', 'Hometown', 'Northland', '1234'),
(10011, 'Apt 505', '456 Pine Street', '', 'Village', 'Auckland', '5678'),
(10012, 'Unit 10', '789 Elm Avenue', '', 'City Center', 'Waikato', '9012'),
(10013, '', '321 Maple Road', '', 'Riverside', 'Bay-of-Plenty', '3456'),
(10014, 'Suite 500', '101 Cedar Street', '', 'Lakeside', 'Gisborne', '7890'),
(10015, '', '222 Birch Lane', '', 'Hilltop', 'Hawkes-Bay', '2345'),
(10016, 'Unit 3', '333 Spruce Avenue', '', 'Seaside', 'Taranaki', '6789'),
(10017, 'Apt 101', '444 Holly Street', '', 'Mountainside', 'Manawatu-Wanganui', '0123'),
(10018, '', '555 Walnut Road', '', 'Valley', 'Wellington', '4567'),
(10019, 'Suite 200', '666 Fir Lane', '', 'Highland', 'Tasman', '8901'),
(10020, '', '777 Beech Avenue', '', 'Lowland', 'Nelson', '2345'),
(10021, 'Unit 5', '888 Sycamore Street', '', 'Woodland', 'Marlborough', '6789'),
(10022, 'Suite 300', '999 Poplar Road', '', 'Meadow', 'West-Coast', '0123'),
(10023, '', '111 Ash Lane', '', 'Prairie', 'Canterbury', '4567'),
(10024, 'Apt 404', '222 Juniper Avenue', '', 'Garden', 'Otago', '8901'),
(10025, 'Unit 20', '333 Elm Street', '', 'Orchard', 'Southland', '2345'),
(10026, '', '444 Maple Avenue', '', 'Lakeview', 'Outer-Islands', '6789'),
(10027, 'Suite 700', '555 Cedar Lane', '', 'Ridge', 'Southland', '0123'),
(10028, '', '666 Pine Road', '', 'Brookside', 'Otago', '4567'),
(10029, 'Unit 15', '777 Birch Street', '', 'Hillside', 'Canterbury', '8901'),
(10030, '', '888 Elm Lane', '', 'Meadowbrook', 'West-Coast', '2345'),
(10031, 'Apt 202', '999 Oak Avenue', '', 'Countryside', 'Marlborough', '6789'),
(10032, 'Suite 1001', '111 Pine Lane', '', 'Forest', 'Nelson', '0123'),
(10033, '', '222 Cedar Road', '', 'Lakefront', 'Tasman', '4567'),
(10034, 'Unit 5', '333 Elm Street', '', 'Riverfront', 'Wellington', '8901'),
(10035, '', '444 Maple Avenue', '', 'Hillcrest', 'Southland', '2345'),
(10036, 'Suite 700', '555 Oak Lane', '', 'Riverside', 'Otago', '6789'),
(10037, '', '666 Pine Street', '', 'Valley View', 'Nelson', '0123'),
(10038, 'Apt 404', '777 Cedar Road', '', 'Sunset', 'Otago', '4567');



INSERT INTO Customers (user_id, first_name, last_name, phone, address_id, points, credit_limit, register_date) VALUES 
(10010, 'Mark', 'Thompson', '02112345678', 16, 0, 0, '2024-05-01'),
(10011, 'Laura', 'White', '02198765432', 17, 0, 0, '2024-04-01'),
(10012, 'Ryan', 'Garcia', '02198765432', 18, 0, 0, '2024-04-01'),
(10013, 'olivia', 'Martinez', '02198765452', 19, 0, 0, '2024-02-01'),
(10014, 'Jacob', 'Robinson', '0219872432', 20, 0, 0, '2024-06-01'),
(10015, 'Ava', 'Clark', '02198765432', 21, 0, 0, '2024-06-01'),
(10016, 'Nathan', 'Hall', '02198769432', 22, 0, 0, '2024-06-01'),
(10017, 'Mia', 'Thomas', '0219665432', 23, 0, 0, '2024-06-01'),
(10018, 'Ethan', 'Lopez', '02198765434', 24, 0, 0, '2024-06-01'),
(10019, 'Ava', 'Hernandez', '02198765432', 25, 0, 0, '2024-06-01'),
(10020, 'Mason', 'Mitchell', '02198795432', 26, 0, 0, '2024-03-01'),
(10021, 'Emma', 'Perez', '02198765432', 27, 0, 0, '2024-06-01'),
(10022, 'Noah', 'Gonzalez', '0219885432', 28, 0, 0, '2024-06-01'),
(10023, 'Isabella', 'Roberts', '0219876582', 29, 0, 0, '2024-06-01'),
(10024, 'Oliver', 'Hill', '02198735432', 30, 0, 0, '2024-06-01'),
(10025, 'Sophia', 'Howard', '02198765432', 31, 0, 0, '2024-04-01'),
(10026, 'Jackson', 'Ramirez', '02198765432', 32, 0, 0, '2024-05-01'),
(10027, 'Amelia', 'Yang', '0219876132', 33, 0, 0, '2024-06-01'),
(10028, 'Aiden', 'Gomez', '02198765432', 34, 0, 0, '2024-06-01'),
(10029, 'Mia', 'Kelly', '02198765432', 35, 0, 0, '2024-06-01'),
(10030, 'Lucas', 'Bailey', '02198765132', 36, 0, 0, '2024-01-01'),
(10031, 'Harper', 'Russell', '02198765432', 37, 0, 0, '2024-01-01'),
(10032, 'Daniel', 'Kim', '02198765422', 38, 0, 0, '2024-06-01'),
(10033, 'Evelyn', 'Fernandez', '02198765472', 39, 0, 0, '2024-06-01'),
(10034, 'Logan', 'Walker', '02198765832', 40, 0, 0, '2024-05-01'),
(10035, 'Ella', 'Cook', '02198765472', 41, 0, 0, '2024-06-01'),
(10036, 'Carter', 'Morris', '02198765432', 42, 0, 0, '2024-06-01'),
(10037, 'Avery', 'Nguyen', '02198767432', 43, 0, 0, '2024-06-01'),
(10038, 'Jack', 'Gonzales', '022111222333', 44, 0, 0, '2024-06-01');




INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status, processor_id, shipping_address) VALUES 
(10009, '2024-05-25', 200.00, 3, 'ready', 1, 'Pick-up');

INSERT INTO Payments (user_id,order_id, payment_amount, payment_date_time, payment_type_id) VALUES 
(10009, LAST_INSERT_ID(),  200.00, '2024-05-23 18:00:00', 1);


INSERT INTO Order_Details (order_id, product_id, product_name,  quantity, unit_price, final_unit_price) VALUES 
(LAST_INSERT_ID(), 10001, 'Mineral Supplements for Cattle', 1, 200.00, 200.00);





INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) VALUES 
(10007, '2024-05-23', 100.00, 3, 'placed',  1, 'Pick-up');


INSERT INTO Order_Details (order_id, product_id, product_name,  quantity, unit_price, final_unit_price) VALUES 
(LAST_INSERT_ID(), 10008, 'Steel Toe Boots', 1, 100.00, 100.00);




INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 

(10007, '2024-05-01', 50.00, 1, 'placed', 2, '456 Elm St, Townsville, Region Y, 5678');

INSERT INTO Order_Details (order_id, product_id, product_name,  quantity, unit_price, final_unit_price) VALUES 
(LAST_INSERT_ID(), 10008, 'Steel Toe Boots', 1, 50.00, 50.00);



INSERT INTO Payments (user_id, order_id, payment_amount, payment_date_time, payment_type_id) 
VALUES 
(10007, LAST_INSERT_ID(), 50.00, '2024-05-06 12:00:00', 1);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10000, '2024-05-02', 125.00, 2, 'placed',  2, '789 Oak St, Villagetown, Region Z, 9012');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 

(LAST_INSERT_ID(), 10001, 'Mineral Supplements for Cattle', 2, 25.00, 50.00),
(LAST_INSERT_ID(), 10002, 'Milking Machine', 1, 75.00, 75.00);
INSERT INTO Payments (user_id, order_id, payment_amount, payment_date_time, payment_type_id) 
VALUES 
(10000, LAST_INSERT_ID(), 125.00, '2024-05-05 12:00:00', 1);

INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10000, '2024-05-02', 125.00, 2, 'placed',  2, '789 Oak St, Villagetown, Region Z, 9012');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 

(LAST_INSERT_ID(), 10001, 'Mineral Supplements for Cattle', 2, 25.00, 50.00),
(LAST_INSERT_ID(), 10002, 'Milking Machine', 1, 75.00, 75.00);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10008, '2024-05-02', 125.00, 2, 'placed',  2, '789 Oak St, Villagetown, Region Z, 9012');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 

(LAST_INSERT_ID(), 10001, 'Mineral Supplements for Cattle', 2, 25.00, 50.00),
(LAST_INSERT_ID(), 10002, 'Milking Machine', 1, 75.00, 75.00);
INSERT INTO Payments (user_id, order_id, payment_amount, payment_date_time, payment_type_id) 
VALUES 
(10008, LAST_INSERT_ID(), 125.00, '2024-05-05 12:00:00', 1);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status, processor_id, shipping_address) 
VALUES 
(10009, '2024-05-03', 125.00, 1, 'placed',  2, '321 Pine St, Hamletville, Region W, 3456');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10001, 'Mineral Supplements for Cattle', 2, 25.00, 50.00),
(LAST_INSERT_ID(), 10002, 'Milking Machine', 1, 75.00, 75.00);

INSERT INTO Payments (user_id, order_id, payment_amount, payment_date_time, payment_type_id) 
VALUES 
(10009, LAST_INSERT_ID(), 125.00, '2024-05-04 12:00:00', 1);

INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10010, '2024-05-04', 125.00, 3, 'placed',  2, '654 Maple St, Countryside, Region V, 7890');
INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10001, 'Mineral Supplements for Cattle', 2, 25.00, 50.00),
(LAST_INSERT_ID(), 10002, 'Milking Machine', 1, 75.00, 75.00);



INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10011, '2024-05-05', 125.00, 2, 'placed',  2, '987 Cedar St, Riverside, Region U, 1234');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10001, 'Mineral Supplements for Cattle', 2, 25.00, 50.00),
(LAST_INSERT_ID(), 10002, 'Milking Machine', 1, 75.00, 75.00);

INSERT INTO Payments (user_id, order_id, payment_amount, payment_date_time, payment_type_id) 
VALUES 
(10011, LAST_INSERT_ID(), 125.00, '2024-05-01 12:00:00', 1);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10012, '2024-05-06', 55.00, 2, 'preparing',  2, '123 Birch St, Hilltown, Region T, 5678');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 

(LAST_INSERT_ID(), 10003, 'Calving Pen', 1, 55.00, 55.00);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10013, '2024-05-07', 70.00, 3, 'preparing',  2, '456 Spruce St, Laketown, Region S, 9012');


INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10004, 'Cattle Crush', 1, 70.00, 70.00);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10015, '2024-05-09', 95.00, 2, 'preparing',  2, '321 Beech St, Lowertown, Region Q, 7890');


INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 

(LAST_INSERT_ID(), 10005, 'Water Storage Tank', 1, 95.00, 95.00);

INSERT INTO Payments (user_id, order_id, payment_amount, payment_date_time, payment_type_id) 
VALUES 
(10015, LAST_INSERT_ID(), 95.00, '2024-05-03 12:00:00', 1);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10016, '2024-05-10', 100.00, 1, 'preparing',  2, '654 Juniper St, Uppertown, Region P, 1234');


INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 

(LAST_INSERT_ID(), 10006, 'Barbed Wire', 1, 100.00, 100.00);

INSERT INTO Payments (user_id, order_id, payment_amount, payment_date_time, payment_type_id) 
VALUES 
(10016, LAST_INSERT_ID(), 100.00, '2024-05-07 12:00:00', 1);





INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status, processor_id, shipping_address) 
VALUES 
(10018, '2024-05-12', 120.00, 1, 'pending', 2, '123 Pine St, Villagetown, Region N, 9012');


INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 

(LAST_INSERT_ID(), 10007, 'Farm Overalls', 1, 120.00, 120.00);


INSERT INTO Payments (user_id, order_id, payment_amount, payment_date_time, payment_type_id) 
VALUES 
(10018, LAST_INSERT_ID(), 120.00, '2024-05-02 12:00:00', 1);





INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10019, '2024-05-13', 130.00, 2, 'pending', 2, '456 Maple St, Townsville, Region M, 3456');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10014, 'NPK Fertilizer', 1, 130.00, 130.00);



INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10020, '2024-05-14', 140.00, 3, 'pending',  2, '789 Cedar St, Hamletville, Region L, 7890');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10006, 'Barbed Wire', 1, 140.00, 140.00);



INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10021, '2024-05-15', 150.00, 1, 'pending',  2, '321 Spruce St, Countryside, Region K, 1234');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10006, 'Barbed Wire', 1, 150.00, 150.00);



INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10022, '2024-05-16', 160.00, 2, 'ready',  2, '654 Fir St, Riverside, Region J, 5678');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10007, 'Farm Overalls', 2, 80.00, 160.00);



INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status, processor_id, shipping_address) 
VALUES 
(10023, '2024-05-17', 170.00, 3, 'ready',  2, '987 Beech St, Hilltown, Region I, 9012');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10008, 'Steel Toe Boots', 1, 170.00, 170.00);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10024, '2024-05-18', 180.00, 1, 'ready',  2, '123 Juniper St, Laketown, Region H, 3456');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10009, 'Cleaning Detergent', 1, 180.00, 180.00);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10025, '2024-05-19', 190.00, 2, 'ready', 2, '456 Elm St, Highlandtown, Region G, 7890');

INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10010, 'Garden Hose', 1, 190.00, 190.00);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10026, '2024-05-20', 200.00, 3, 'ready', 2, '789 Birch St, Lowertown, Region F, 1234');
INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10006, 'Barbed Wire', 1, 200.00, 200.00);

INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10027, '2024-06-01', 210.00, 1, 'finished',  2, '321 Spruce St, Uppertown, Region E, 5678');
INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10011, 'Herbicide Spray', 1, 110.00, 110.00),
(LAST_INSERT_ID(), 10001, 'Herbicide Spray', 1, 200.00, 200.00)
;

INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10028, '2024-05-22', 220.00, 2, 'finished',  2, '654 Elm St, Citytown, Region D, 9012');
INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10012, 'Tractor', 1, 220.00, 220.00);


INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10029, '2024-05-23', 220.00, 3, 'finished',  2, '987 Pine St, Villagetown, Region C, 3456');
INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10013, 'Grass Seeds', 2, 110.00, 220.00);

INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status,  processor_id, shipping_address) 
VALUES 
(10030, '2024-05-24', 240.00, 1, 'finished',  2, '123 Maple St, Townsville, Region B, 7890');
INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10014, 'NPK Fertilizer', 1, 240.00, 240.00);

INSERT INTO Orders (user_id, order_date, total_amount, shipping_method_id, order_status, processor_id, shipping_address) 
VALUES 
(10031, '2024-06-05', 250.00, 2, 'finished',  2, '456 Cedar St, Hamletville, Region A, 1234');
INSERT INTO Order_Details (order_id, product_id, product_name, quantity, unit_price, final_unit_price) 
VALUES 
(LAST_INSERT_ID(), 10005, 'Water Storage Tank', 2, 125.00, 250.00);


INSERT INTO Gift_Cards ( gift_card_number, gift_card_amount, user_id, expiry_date) 
VALUES 
(5843254813575478, 250.00, 10000, '2025-05-21'), 
(5843254813575472, 100.00, 10000, '2026-05-21'), 
(5843254813575473, 0.00, 10000, '2023-05-21'), 
(5843254583575474, 100.00, 10000, '2022-05-21'), 
(5843254813575728, 50.00, 10000, '2025-05-21'), 
(5843254121357578, 30.00, 10000, '2025-05-21');

INSERT INTO Gift_Cards ( gift_card_number, gift_card_amount, expiry_date) 
VALUES 
(5843154121457578, 30.00, '2025-05-21'),
(5113234121357578, 30.00,  '2025-05-21');



INSERT INTO News (sender_id, news_subject, news_content, news_image, news_timestamp, news_status)
VALUES
(3, "New Organic Animal Feed Line Launched", "A leading agricultural company has launched a new line of organic animal feed, promising enhanced nutrition and improved health for livestock.", 'New Organic Animal Feed.png', '2024-06-1 6:00:00', 1), 
(3, "Innovative Dairy Hygiene Solutions Introduced", "Farmers can now access the latest dairy hygiene solutions designed to maintain top-notch milk quality and ensure the health of their dairy herds.", 'Innovative Dairy Hygiene Solutions.jpg', '2024-06-2 7:00:00', 0),
(3, "Advanced Calving Equipment Now Available", "The market sees the introduction of advanced calving equipment that promises to make the birthing process safer and more efficient for both cows and farmers.", 'Advanced Calving Equipment.jpg', '2024-06-3 8:00:00', 0), 
(3, "Smart Water Management Systems for Farms", "New smart water management systems are being adopted by farms to improve water usage efficiency and reduce wastage, ensuring sustainable farming practices.", 'Smart Water Management Systems.jpg', '2024-06-4 9:00:00', 1), 
(3, "High-Performance Clothing for Farmers Released", "A new range of high-performance clothing tailored for farmers has been released, offering enhanced comfort and protection during long working hours.", 'High-Performance Clothing.jpg', '2024-06-5 10:00:00', 0), 
(3, "Sustainable Household Supplies for Rural Homes", "The latest eco-friendly household supplies are now on the market, catering specifically to the needs of rural homes and promoting sustainable living.", 'Sustainable Household Supplies.jpg', '2024-06-6 11:00:00', 0), 
(3, "Garden Supplies Market Sees New Additions", "Innovative garden supplies, including advanced tools and organic fertilizers, are now available to help farmers and gardeners enhance their productivity.", 'Garden Supplies Market.png', '2024-06-7 12:00:00', 1), 
(3, "High-Efficiency Machinery & Oil Now in Stock", "High-efficiency machinery and oil products have hit the shelves, promising to increase farm productivity and reduce maintenance costs.", 'High-Efficiency Machinery & Oil.jpg', '2024-06-8 13:00:00', 1);


INSERT INTO Product_Images (product_id, product_image) VALUES 
(10010, 'images-garden-hose.jpg'),
(10008, 'boot-image-2.jpg'),
(10025, 'seeds-page-hero.jpg'),
(10022, '2DF_800.jpg'),
(10012, 'images-tractor2.jpg'),
(10000, 'images-anti-2.jpg'),
(10006, 'Barbed Wire1.jpg'),
(10003, 'Calving Pen1.jpg'),
(10004, 'Cattle Crush1.jpg'),
(10009, 'Cleaning Detergent1.jpg'),
(10015, 'Drench for Sheep1.jpg'),
(10007, 'Farm Overalls1.jpg'),
(10013, 'Grass Seeds1.jpg'),
(10011, 'Herbicide Spray1.jpg'),
(10002, 'Milking Machine1.jpg'),
(10001, 'Mineral Supplements for Cattle1.jpg'),
(10014, 'NPK Fertilizer1.jpg'),
(10016, 'Vitamin Supplements for Pigs1.jpg'),
(10005, 'Water Storage Tank1.jpg');
