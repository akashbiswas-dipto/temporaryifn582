from dataclasses import dataclass, field
from enum import Enum

class ProductCategory(Enum):
    FIRSTAID = 'First-aid'
    COLDFLU = 'Cold and Flu'
    PAINRELIEF = 'Pain Relief'

@dataclass
class Product:
    id: str
    title: str
    description: str
    category: ProductCategory
    image: str
    price: float

@dataclass
class UserInfo:
    id: str
    firstname: str
    surname: str
    email: str
    phone: str
    username: str




