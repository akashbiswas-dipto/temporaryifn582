from medifast.db import get_product
from medifast.models import UserInfo, ShoppingCart, ShoppingCartItem, Product, Order
from uuid import uuid4
from flask import session

def get_user():
    user = session.get('user')
    if user:
        print("user:", user)
        return UserInfo(
            id=str(user['id']),
            firstname=user['firstname'],
            surname=user['surname'],
            email=user['email'],
            phone=user['phone'],
            username=user['username'],
            password="",
            user_type=user['user_type']
        )
    return None
    
def get_shoppingcart():
    shoppingcart_data = session.get("shoppingcart")
    print("get_shoppingcart:", shoppingcart_data)
    shoppingcart = ShoppingCart()
    print(isinstance(shoppingcart_data, dict))
    print(type(shoppingcart_data))
    if isinstance(shoppingcart_data, dict):
        for item in shoppingcart_data.get('items', []):
            product = get_product(item['product'])
            print("product from db", product)
            print("item", item)
            if product:
                shoppingcart.add_item(ShoppingCartItem(
                    id=item['id'],
                    product=product,
                    quantity=item["quantity"]
                ))
    return shoppingcart

def _save_shoppingcart_to_session(shoppingcart):
    session['shoppingcart'] = {
        'items': [
            {
                'id': item.id,
                'quantity': item.quantity,
                'product': item.product.id
            } for item in shoppingcart.items
        ]
    }

def add_to_shoppingcart(product_id, quantity=1):
    shoppingcart = get_shoppingcart()
    shoppingcart.add_item(ShoppingCartItem(product=get_product(product_id), quantity=quantity))
    _save_shoppingcart_to_session(shoppingcart)

def update_item_from_shoppingcart(product_id,quantity):
    shoppingcart = get_shoppingcart()
    item = shoppingcart.get_item(product_id)
    item.edit_quantity(quantity)
    _save_shoppingcart_to_session(shoppingcart)

def remove_from_shoppingcart(shoppingcart_item_id):
    shoppingcart = get_shoppingcart()
    shoppingcart.remove_item(shoppingcart_item_id)
    _save_shoppingcart_to_session(shoppingcart)

def empty_shoppingcart():
    session['shoppingcart'] = {
        'items': []
    }

def shoppingcart_to_order(form, shoppingcart, user_id, order_datetime):
    print("entered session", user_id, form.delivery_type.data, shoppingcart.items)
    print("form value", form.delivery_type.data, form.payment_type.data, form.address.data, form.customer_phone.data, form.customer_email.data, form.customer_name.data)
    print(shoppingcart.total_cost())
    order =  Order(
        id="",
        status=0,
        user_id=user_id,
        amount=shoppingcart.total_cost(),
        delivery_type=int(form.delivery_type.data),
        address=form.address.data,
        payment_type=int(form.payment_type.data),
        customer_name=form.customer_name.data,
        customer_phone=form.customer_phone.data,
        customer_email=form.customer_email.data,
        items=shoppingcart.items, 
        date=order_datetime
    )
    print(order)
    return order 

def get_order():
    pass