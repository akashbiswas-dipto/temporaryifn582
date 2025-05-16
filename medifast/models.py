from dataclasses import dataclass, field
from enum import Enum

@dataclass
class UserInfo:
    id: str
    firstname: str
    surname: str
    email: str
    phone: str
    username: str

@dataclass
class UserAccount:
    email: str
    password: str
    username: str
    info: UserInfo

@dataclass
class Product:
    id: str
    title: str
    description: str
    category: str
    image: str
    price: float

class productCategory(Enum):
    FIRSTAID = 'First-aid'
    COLDFLU = 'Cold and Flu'
    PAINRELIEF = 'Pain Relief'

