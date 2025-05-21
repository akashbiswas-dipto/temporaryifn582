from dataclasses import dataclass, field


@dataclass
class Product:
    id: str
    title: str
    description: str
    category: str
    stock: int
    img: str
    price: float

@dataclass
class UserInfo:
    id: str
    firstname: str
    surname: str
    email: str
    phone: str
    username: str
    password: str
    role: str




