from medifast.models import UserInfo, Product
from werkzeug.security import check_password_hash
from datetime import datetime
from . import mysql

def check_for_user(email, password):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, firstname, surname, email, phone, phone, username, password, user_type
        FROM users
        WHERE email = %s AND password = %s
    """, (email, password))
    row = cur.fetchone()
    print("db", row)
    cur.close()
    if row:
        return UserInfo(str(row['id']), row['firstname'], row['surname'], row['email'], row['phone'],row['username'], row['password'],row['user_type'])
    return None

def add_user(form, hashed):
    user_type = "0"
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO users (username, password, email, firstname, surname, phone, user_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (form.username.data, hashed, form.email.data,
          form.firstname.data, form.surname.data, form.phone.data, user_type))
    mysql.connection.commit()
    cur.close()

def add_login_record(user_id):
    login_time = datetime.now()
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO login_record (user_id, login_time) values (%s,%s)""", (user_id, login_time))
    mysql.connection.commit()
    cur.close() 

def add_logout_record(user_id):
    logout_time = datetime.now()
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO login_record (logout_time) values (%s) WHERE user_id = %s and logout_time is null """, (logout_time, user_id))
    mysql.connection.commit()
    cur.close() 

def get_products():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, name, description, price, category, quantity, keyword, prescription, img1, img2,img3 
        FROM products
    """)
    rows = cur.fetchall()
    cur.close()
    return [Product(str(row['id']), row['name'], row['description'], row['price'], row['category'], row['quantity'], row['keyword'],row['prescription'], row['img1'], row['img2'],row['img3']) for row in rows] 
    
def get_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, name, description, price, category, quantity, keyword, prescription, img1, img2,img3 
        FROM products WHERE id = %s
    """, (product_id,))
    row = cur.fetchone()
    cur.close()
    return Product(str(row['id']), row['name'], row['description'], row['price'], row['category'], row['quantity'], row['keyword'],row['prescription'], row['img1'], row['img2'],row['img3'])


def add_order(form, user_id):
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO orders (user_id, product_id, amount, order_date, delivery_type, address, payment_type, order_status, customer_name, customer_email, customer_phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (user_id, ))
    return str()

def get_order(user_id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * from orders where user_id = %s""", (user_id,))
    row = cur.fetchAll()
    cur.close()
    return    