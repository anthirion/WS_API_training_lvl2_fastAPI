-- init.sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    productName VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(255) NOT NULL,
    stock INT NOT NULL
);

INSERT INTO products (productName, description, price, category, stock) VALUES
("Smartwatch Alpha", "Une montre intelligente avec des fonctionnalites avancees de suivi de la sante.", 199.99, "Electronique", 150),
("Cafe Gourmet", "Un melange exquis de grains de cafe biologiques provenant des meilleures plantations.", 15.50, "Alimentation", 300),
("Chaise de Bureau Ergonomique", "Chaise de bureau avec soutien lombaire ajustable et accoudoirs confortables.", 129.99, "Mobilier", 75),
("Sac a Dos de Randonnee", "Sac a dos durable et spacieux avec plusieurs compartiments pour le trekking.", 89.95, "Sport et Plein Air", 200),
("Serum Anti-age", "Serum haut de gamme pour reduire les rides et ameliorer la texture de la peau.", 49.99, "Beaute", 500);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO users (username, email, address, password) VALUES
("Alice", "alice@example.com", "123 Apple St Wonderland", "password123"),
("Bob", "bob@example.com", "456 Orange Ave Fruitland", "bobspassword"),
("Charlie", "charlie@example.com", "789 Banana Blvd Tropicland", "charliepass"),
("Diana", "diana@example.com", "321 Grape Rd Vineyard", "dianasecret"),
("Eve", "eve@example.com", "654 Peach Ln Orchard", "evepassword");

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    total FLOAT NOT NULL,
    status VARCHAR(255) NOT NULL,
    FOREIGN KEY (userId) REFERENCES users(id)
);

INSERT INTO orders (userId, total, status) VALUES
(1, 45.97, "Completed"),
(2, 23.97, "Pending"),
(3, 299.99, "Shipped"),
(1, 17.45, "Cancelled"),
(2, 76.98, "Processing");

CREATE TABLE orderlines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    productId INT NOT NULL,
    orderedQuantity INT NOT NULL,
    orderId INT NOT NULL,
    unitPrice DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (productId) REFERENCES products(id),
    FOREIGN KEY (orderId) REFERENCES orders(id)
);

INSERT INTO orderlines (productId, orderedQuantity, orderId, unitPrice) VALUES
(2, 1, 1, 199.99),
(4, 3, 1, 129.99),
(3, 2, 2, 15.50),
(5, 1, 3, 199.99),
(1, 3, 4, 129.99),
(1, 3, 5, 129.99),
(4, 2, 5, 15.50);