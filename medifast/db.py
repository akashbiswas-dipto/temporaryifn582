from medifast.models import UserInfo, Product, Order
from werkzeug.security import check_password_hash
from datetime import datetime
from . import mysql
import MySQLdb

def search(query):
    cur = mysql.connection.cursor()
    q = f"%{query}%"
    cur.execute("SELECT * FROM product WHERE name LIKE %s OR keyword LIKE %s OR category LIKE %s", (q, q, q))
    rows = cur.fetchall()
    cur.close()
    return [Product(str(row['id']), row['name'], row['description'], row['price'], row['quantity'], row['category'], row['keyword'],row['prescription'], row['img1'], row['img2'],row['img3']) for row in rows] 
    

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

def admin_check_for_user():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(""" SELECT * FROM users """)
    rows = cur.fetchall()
    print("db", rows)
    cur.close()
    users = []
    if rows:
        for row in rows:
            user = UserInfo(
                str(row['id']),
                row['firstname'],
                row['surname'],
                row['email'],
                row['phone'],
                row['username'],
                row['password'],
                row['user_type']
            )
            users.append(user)
    return users


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
    cur.execute("""UPDATE login_record set logout_time=(%s) WHERE user_id = %s and logout_time is null ORDER BY login_time desc """, (logout_time, user_id))
    mysql.connection.commit()
    cur.close() 

def get_products():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT * FROM product
    """)
    rows = cur.fetchall()
    cur.close()
    return [Product(str(row['id']), row['name'], row['description'], row['price'], row['quantity'], row['category'], row['keyword'],row['prescription'], row['img1'], row['img2'],row['img3']) for row in rows] 
   
def get_product(product_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, name, description, price, category, quantity, keyword, prescription, img1, img2,img3 
        FROM product WHERE id = %s
    """, (product_id,))
    row = cur.fetchone()
    cur.close()
    return Product(str(row['id']), row['name'], row['description'], row['price'], row['category'], row['quantity'], row['keyword'],row['prescription'], row['img1'], row['img2'],row['img3'])


def add_order(order: Order):
    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO orders (amount, order_date, address, delivery_type, payment_type, order_status, customer_name, customer_email, customer_phone) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (order.amount, order.date,order.address,order.delivery_type, order.payment_type, order.status, order.customer_name, order.customer_email, order.customer_phone ))
    order_id = cur.lastrowid

    for item in order.items:
        cur.execute("INSERT INTO order_items (user_id, order_id, product_id, quantity) VALUES (%s,%s,%s,%s)", (order.user_id, order_id, item.product.id, item.quantity))
    mysql.connection.commit()
    cur.close()

# def get_order(user_id):
#     cur = mysql.connection.cursor()
#     cur.execute("""SELECT * from orders o JOIN product p ON o.product_id = p.id where o.user_id = %s""", (user_id,))
#     rows = cur.fetchAll()
#     cur.close()
#     return  [Order(str(row['id'], OrderStatus(row['order_status']), row['user_id'], row['amount'], row['delivery_type'], row['payment_type'], row['address'], row['customer_name'], row['customer_phone'], row['customer_email'], [Product(row[])], row['order_date'], ), ) for row in rows]  