from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    stock: int


all_products = [
    Product(
        id=1,
        name="Smartwatch Alpha",
        description="Une montre intelligente avec des fonctionnalités avancées de suivi de la santé.",
        price=199.99,
        category="Électronique",
        stock=150
    ),
    Product(
        id=2,
        name="Café Gourmet",
        description="Un mélange exquis de grains de café biologiques provenant des meilleures plantations.",
        price=15.50,
        category="Alimentation",
        stock=300
    ),
    Product(
        id=3,
        name="Chaise de Bureau Ergonomique",
        description="Chaise de bureau avec soutien lombaire ajustable et accoudoirs confortables.",
        price=129.99,
        category="Mobilier",
        stock=75
    ),
    Product(
        id=4,
        name="Sac à Dos de Randonnée",
        description="Sac à dos durable et spacieux avec plusieurs compartiments pour le trekking.",
        price=89.95,
        category="Sport et Plein Air",
        stock=200
    ),
    Product(
        id=5,
        name="Sérum Anti-Âge",
        description="Sérum haut de gamme pour réduire les rides et améliorer la texture de la peau.",
        price=49.99,
        category="Beauté",
        stock=500
    )
]
