"""
This module defines a list of products
"""

from .schemas import Product, User, Order, Item

all_products = [
    Product(
        id=1,
        product_name="Smartwatch Alpha",
        description="Une montre intelligente avec des fonctionnalites avancees de suivi de la sante.",
        price=199.99,
        category="Electronique",
        stock=150
    ),
    Product(
        id=2,
        product_name="Cafe Gourmet",
        description="Un melange exquis de grains de cafe biologiques provenant des meilleures plantations.",
        price=15.50,
        category="Alimentation",
        stock=300
    ),
    Product(
        id=3,
        product_name="Chaise de Bureau Ergonomique",
        description="Chaise de bureau avec soutien lombaire ajustable et accoudoirs confortables.",
        price=129.99,
        category="Mobilier",
        stock=75
    ),
    Product(
        id=4,
        product_name="Sac a Dos de Randonnee",
        description="Sac a dos durable et spacieux avec plusieurs compartiments pour le trekking.",
        price=89.95,
        category="Sport et Plein Air",
        stock=200
    ),
    Product(
        id=5,
        product_name="Serum Anti-age",
        description="Serum haut de gamme pour reduire les rides et ameliorer la texture de la peau.",
        price=49.99,
        category="Beaute",
        stock=500
    )
]

all_users = [
    User(id=1,
         username="Alice",
         email="alice@example.com",
         address="123 Apple St Wonderland",
         password="password123"),
    User(id=2,
         username="Bob",
         email="bob@example.com",
         address="456 Orange Ave Fruitland",
         password="bobspassword"),
    User(id=3,
         username="Charlie",
         email="charlie@example.com",
         address="789 Banana Blvd Tropicland",
         password="charliepass"),
    User(id=4,
         username="Diana",
         email="diana@example.com",
         address="321 Grape Rd Vineyard",
         password="dianasecret"),
    User(id=5,
         username="Eve",
         email="eve@example.com",
         address="654 Peach Ln Orchard",
         password="evepassword")
]

all_orders = [
    Order(
        id=1,
        user_id=1,
        items=[
            Item(product_id=2, ordered_quantity=2, unit_price=15.50),
            Item(product_id=4, ordered_quantity=1, unit_price=89.95),
        ],
        total=120.95,
        status="Completed"
    ),
    Order(
        id=2,
        user_id=2,
        items=[
            Item(product_id=3, ordered_quantity=2, unit_price=15.50),
        ],
        total=31,
        status="Pending"
    ),
    Order(
        id=3,
        user_id=3,
        items=[
            Item(product_id=5, ordered_quantity=1, unit_price=89.95),
        ],
        total=89.95,
        status="Shipped"
    ),
    Order(
        id=4,
        user_id=1,
        items=[
            Item(product_id=1, ordered_quantity=3, unit_price=199.99),
        ],
        total=599.97,
        status="Cancelled"
    ),
    Order(
        id=5,
        user_id=2,
        items=[
            Item(product_id=1, ordered_quantity=2, unit_price=199.99),
            Item(product_id=5, ordered_quantity=3, unit_price=49.99),
        ],
        total=549.95,
        status="Pending"
    )
]
