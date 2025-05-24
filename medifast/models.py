from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List
from uuid import uuid4

class OrderStatus(Enum):
    PENDING = 1
    CONFIRMED = 2
    CANCELLED = 3

@dataclass
class Product:
    id: str
    name: str
    description: str
    price: float
    stock_qty: int
    category: str
    keyword: str
    prescription: str
    img1: str
    img2: str
    img3: str
    

@dataclass
class UserInfo:
    id: str
    firstname: str
    surname: str
    email: str
    phone: str
    username: str
    password: str
    user_type: int

# shoppingcart item
@dataclass 
class ShoppingCartItem:
    product: Product
    quantity: int = 1
    id: str = field(default_factory=lambda: str(uuid4()))

    def total_price(self):
        return self.product.price * self.quantity
    
    def increment_quantity(self):
        self.quantity += 1

    def decrement_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1

@dataclass
class ShoppingCart:
    items: List[ShoppingCartItem] = field(default_factory=lambda: [])

    def add_item(self, item: Product):
        self.items.append(item)

    def remove_item(self, item_id: str):
        self.items = [item for item in self.items if item.id != item_id]

    def get_item(self, item_id: str):
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def empty(self):
        self.items = []
    
    def total_cost(self):
        return sum(item.total_price() for item in self.items)

@dataclass
class Order:
    id: str
    status: OrderStatus
    user: UserInfo
    amount: float = 0.0
    items: List[ShoppingCartItem] = field(default_factory=list)
    date: datetime = field(default_factory=lambda: datetime.now())




