from medifast.models import UserInfo, Product
from werkzeug.security import check_password_hash
from datetime import datetime
from . import mysql

def check_for_user(email):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, firstname, surname, email, phone, username, password,role
        FROM users
        WHERE email = %s
    """, (email,))
    row = cur.fetchone()
    print("db", row)
    cur.close()
    if row:
        return UserInfo(str(row['id']), row['firstname'], row['surname'], row['email'], row['phone'],row['username'], row['password'],row['role'])
    return None

def add_user(form, hashed):
    role = "user"
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO users (username, password, email, firstname, surname, phone,role)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (form.username.data, hashed, form.email.data,
          form.firstname.data, form.surname.data, form.phone.data, role))
    mysql.connection.commit()
    cur.close()

def get_product():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, title, description, category, stock, img, price 
        FROM product 
    """)
    results = cur.fetchall()
    cur.close()
    return [
        Product(str(row['id']), row['title'], row['description'], row['category'], row['stock'], row['img'],row['price']) for row in results
    ]