-- This script is used to configure MS SQL Server DB on Azure
-- It is the same script as init-mysql.sql except the database name and the target query language (MS SQL Server)

-- Check if database exists, if not create it
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'ws-api-training-shop-db')
BEGIN
    CREATE DATABASE [ws-api-training-shop-db];
END
GO

USE [ws-api-training-shop-db];
GO

-- PRODUCTS Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'products')
BEGIN
    CREATE TABLE products (
        id INT PRIMARY KEY,
        product_name NVARCHAR(255) NOT NULL,
        description NVARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        category NVARCHAR(255) NOT NULL,
        stock INT NOT NULL
    );
END
GO

-- Insert data only if the table is empty
IF (SELECT COUNT(*) FROM products) = 0
BEGIN
    INSERT INTO products (id, product_name, description, price, category, stock)
    VALUES
        (1, N'Smartwatch Alpha', N'Une montre intelligente avec des fonctionnalites avancees de suivi de la sante.', 199.99, N'Electronique', 150),
        (2, N'Cafe Gourmet', N'Un melange exquis de grains de cafe biologiques provenant des meilleures plantations.', 15.50, N'Alimentation', 300),
        (3, N'Chaise de Bureau Ergonomique', N'Chaise de bureau avec soutien lombaire ajustable et accoudoirs confortables.', 129.99, N'Mobilier', 75),
        (4, N'Sac a Dos de Randonnee', N'Sac a dos durable et spacieux avec plusieurs compartiments pour le trekking.', 89.95, N'Sport et Plein Air', 200),
        (5, N'Serum Anti-age', N'Serum haut de gamme pour reduire les rides et ameliorer la texture de la peau.', 49.99, N'Beaute', 500);
END
GO

-- USERS Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
BEGIN
    CREATE TABLE users (
        id INT PRIMARY KEY,
        username NVARCHAR(255) NOT NULL,
        email NVARCHAR(255) NOT NULL,
        address NVARCHAR(255) NOT NULL,
        password NVARCHAR(255) NOT NULL
    );
END
GO

-- Insert data only if the table is empty
IF (SELECT COUNT(*) FROM users) = 0
BEGIN
    INSERT INTO users (id, username, email, address, password)
    VALUES
        (1, N'Alice', N'alice@example.com', N'123 Apple St Wonderland', N'password123'),
        (2, N'Bob', N'bob@example.com', N'456 Orange Ave Fruitland', N'bobspassword'),
        (3, N'Charlie', N'charlie@example.com', N'789 Banana Blvd Tropicland', N'charliepass'),
        (4, N'Diana', N'diana@example.com', N'321 Grape Rd Vineyard', N'dianasecret'),
        (5, N'Eve', N'eve@example.com', N'654 Peach Ln Orchard', N'evepassword');
END
GO

-- ORDERS Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'orders')
BEGIN
    CREATE TABLE orders (
        id INT PRIMARY KEY,
        user_id INT NOT NULL,
        total FLOAT NOT NULL,
        status NVARCHAR(255) NOT NULL,
        CONSTRAINT FK_orders_users FOREIGN KEY (user_id) REFERENCES users(id)
    );
END
GO

-- Insert data only if the table is empty
IF (SELECT COUNT(*) FROM orders) = 0
BEGIN
    INSERT INTO orders (id, user_id, total, status)
    VALUES
        (1, 1, 45.97, N'Completed'),
        (2, 2, 23.97, N'Pending'),
        (3, 3, 299.99, N'Shipped'),
        (4, 1, 17.45, N'Cancelled'),
        (5, 2, 76.98, N'Processing');
END
GO

-- ORDERLINES Table
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'orderlines')
BEGIN
    CREATE TABLE orderlines (
        id INT PRIMARY KEY,
        product_id INT NOT NULL,
        ordered_quantity INT NOT NULL,
        order_id INT NOT NULL,
        unit_price DECIMAL(10, 2) NOT NULL,
        CONSTRAINT FK_orderlines_products FOREIGN KEY (product_id) REFERENCES products(id),
        CONSTRAINT FK_orderlines_orders FOREIGN KEY (order_id) REFERENCES orders(id)
    );
END
GO

-- Insert data only if the table is empty
IF (SELECT COUNT(*) FROM orderlines) = 0
BEGIN
    INSERT INTO orderlines (id, product_id, ordered_quantity, order_id, unit_price)
    VALUES
        (1, 2, 1, 1, 199.99),
        (2, 4, 3, 1, 129.99),
        (3, 3, 2, 2, 15.50),
        (4, 5, 1, 3, 199.99),
        (5, 1, 3, 4, 129.99),
        (6, 1, 3, 5, 129.99),
        (7, 4, 2, 5, 15.50);
END
GO

-- To verify that the script executed successfully, run the following query:
-- SELECT * FROM products;