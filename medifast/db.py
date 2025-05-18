from medifast.models import UserInfo
from werkzeug.security import check_password_hash
from datetime import datetime
from . import mysql

def check_for_user(email, hashed):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, username, firstname, surname, email, phone
        FROM users
        WHERE email = %s AND password = %s
    """, (email, hashed))
    row = cur.fetchone()
    cur.close()
    if row:
        return UserInfo(str(row['id']), row['firstname'], row['surname'], row['username'],row['email'], row['phone'])
    return None

def add_user(form, hashed):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO users (username, password, email, firstname, surname, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (form.username.data, hashed, form.email.data,
          form.firstname.data, form.surname.data, form.phone.data))
    mysql.connection.commit()
    cur.close()
