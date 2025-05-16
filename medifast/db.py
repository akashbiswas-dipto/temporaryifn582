from medifast.models import UserInfo, UserAccount
from datetime import datetime
from . import mysql

def check_for_user(email, password):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, username, password, firstname, surname, email, phone
        FROM users
        WHERE username = %s AND password = %s
    """, (email, password))
    row = cur.fetchone()
    cur.close()
    if row:
        return UserAccount(row['username'], row['password'], row['email'],
                           UserInfo(str(row['id']), row['firstname'], row['surname'],
                                    row['email'], row['phone']))
    return None

def add_user(form):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO users (username, password, email, firstname, surname, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (form.username.data, form.password.data, form.email.data,
          form.firstname.data, form.surname.data, form.phone.data))
    mysql.connection.commit()
    cur.close()
