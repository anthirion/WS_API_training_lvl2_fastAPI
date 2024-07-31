"""
This module defines a list of products
"""

from .schemas import Product

all_products = [
    Product(
        id=1,
        name="Smartwatch Alpha",
        description="Une montre intelligente avec des fonctionnalites avancees de suivi de la sante.",
        price=199.99,
        category="Electronique",
        stock=150
    ),
    Product(
        id=2,
        name="Cafe Gourmet",
        description="Un melange exquis de grains de cafe biologiques provenant des meilleures plantations.",
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
        name="Sac à Dos de Randonnee",
        description="Sac à dos durable et spacieux avec plusieurs compartiments pour le trekking.",
        price=89.95,
        category="Sport et Plein Air",
        stock=200
    ),
    Product(
        id=5,
        name="Serum Anti-age",
        description="Serum haut de gamme pour reduire les rides et ameliorer la texture de la peau.",
        price=49.99,
        category="Beaute",
        stock=500
    )
]
