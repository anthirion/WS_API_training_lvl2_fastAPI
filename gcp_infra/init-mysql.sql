CREATE DATABASE IF NOT EXISTS api_training;
USE api_training;

----------------------------------------------------------------
-- Table PRODUCTS
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(255) NOT NULL,
    stock INT NOT NULL
);

-- insérer des données uniquement si la table est vide
INSERT INTO products (id, product_name, description, price, category, stock)
SELECT 1, "Smartwatch Alpha", "Une montre intelligente avec des fonctionnalites avancees de suivi de la sante.", 199.99, "Electronique", 150
UNION ALL
SELECT 2, "Cafe Gourmet", "Un melange exquis de grains de cafe biologiques provenant des meilleures plantations.", 15.50, "Alimentation", 300
UNION ALL
SELECT 3, "Chaise de Bureau Ergonomique", "Chaise de bureau avec soutien lombaire ajustable et accoudoirs confortables.", 129.99, "Mobilier", 75
UNION ALL
SELECT 4, "Sac a Dos de Randonnee", "Sac a dos durable et spacieux avec plusieurs compartiments pour le trekking.", 89.95, "Sport et Plein Air", 200
UNION ALL
SELECT 5, "Serum Anti-age", "Serum haut de gamme pour reduire les rides et ameliorer la texture de la peau.", 49.99, "Beaute", 500
WHERE (SELECT COUNT(*) FROM products) = 0;

----------------------------------------------------------------
-- Table USERS
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- insérer des données uniquement si la table est vide
INSERT INTO users (id, username, email, address, password)
SELECT 1, "Alice", "alice@example.com", "123 Apple St Wonderland", "password123"
UNION ALL
SELECT 2, "Bob", "bob@example.com", "456 Orange Ave Fruitland", "bobspassword"
UNION ALL
SELECT 3, "Charlie", "charlie@example.com", "789 Banana Blvd Tropicland", "charliepass"
UNION ALL
SELECT 4, "Diana", "diana@example.com", "321 Grape Rd Vineyard", "dianasecret"
UNION ALL
SELECT 5, "Eve", "eve@example.com", "654 Peach Ln Orchard", "evepassword"
WHERE (SELECT COUNT(*) FROM users) = 0;

----------------------------------------------------------------
-- Table ORDERS
CREATE TABLE IF NOT EXISTS orders (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    total FLOAT NOT NULL,
    status VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- insérer des données uniquement si la table est vide
INSERT INTO orders (id, user_id, total, status)
SELECT 1, 1, 45.97, "Completed"
UNION ALL
SELECT 2, 2, 23.97, "Pending"
UNION ALL
SELECT 3, 3, 299.99, "Shipped"
UNION ALL
SELECT 4, 1, 17.45, "Cancelled"
UNION ALL
SELECT 5, 2, 76.98, "Processing"
WHERE (SELECT COUNT(*) FROM orders) = 0;

----------------------------------------------------------------
-- Table ORDERLINES
CREATE TABLE IF NOT EXISTS orderlines (
    id INT PRIMARY KEY,
    product_id INT NOT NULL,
    ordered_quantity INT NOT NULL,
    order_id INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- insérer des données uniquement si la table est vide
INSERT INTO orderlines (id, product_id, ordered_quantity, order_id, unit_price)
SELECT 1, 2, 1, 1, 199.99
UNION ALL
SELECT 2, 4, 3, 1, 129.99
UNION ALL
SELECT 3, 3, 2, 2, 15.50
UNION ALL
SELECT 4, 5, 1, 3, 199.99
UNION ALL
SELECT 5, 1, 3, 4, 129.99
UNION ALL
SELECT 6, 1, 3, 5, 129.99
UNION ALL
SELECT 7, 4, 2, 5, 15.50
WHERE (SELECT COUNT(*) FROM orderlines) = 0;