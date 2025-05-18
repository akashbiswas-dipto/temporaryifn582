from medifast.models import UserInfo

from flask import session

def get_user():
    user = session.get('user')
    if user:
        print("user:", user)
        return UserInfo(
            id=str(user['user_id']),
            firstname=user['firstname'],
            surname=user['surname'],
            email=user['email'],
            phone=user['phone'],
            username=user['username']
        )
    print("user", None)
    return None


