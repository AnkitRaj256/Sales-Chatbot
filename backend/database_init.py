import MySQLdb
import random

# Function to generate mock product data
def generate_product(product_id):
    names = [
        "Laptop", "Smartphone", "Tablet", "Smartwatch", 
        "Headphones", "Bluetooth Speaker", "Camera", 
        "Wireless Charger", "Smart TV", "Monitor", 
        "Keyboard", "Mouse", "USB Drive", "Backpack", 
        "Sneakers", "Jacket", "T-shirt", "Book", 
        "Board Game", "Fitness Tracker", "Coffee Maker"
    ]
    
    name = f"{random.choice(names)} {product_id}"
    price = round(random.uniform(10.0, 2000.0), 2)  # Random price between 10 and 2000
    stock = random.randint(1, 100)  # Random stock between 1 and 100
    category = random.choice([
        "Electronics", "Computers", "Smartphones", "Accessories", 
        "Clothing", "Shoes", "Home & Garden", "Books", 
        "Sports", "Toys", "Health & Beauty"
    ])
    
    return (name, "Sample description", price, stock, category)

# Function to generate mock user data
def generate_user(user_id):
    usernames = [f"user{user_id}", f"testuser{user_id}", f"shopper{user_id}"]
    password = "password123"  # Default password for mock users
    return (random.choice(usernames), password)

# Function to generate mock chat data for a user
def generate_chat(user_id):
    messages = [
        "Hello, I need help with my order.",
        "Can you tell me more about the smartphone?",
        "How do I return this product?",
        "What is the status of my refund?",
        "I am interested in buying a new laptop.",
        "Can you assist me with the shipping details?",
        "What products are on sale this week?",
        "Do you have any discounts available?"
    ]
    message = random.choice(messages)
    return (user_id, message)

# Database setup
connection = MySQLdb.connect(
    host="localhost",
    user="root",  # Your MySQL username
    password="Ankit@SQL25",  # Your MySQL password
)

cursor = connection.cursor()

# Create database and use it
cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce_db")
cursor.execute("USE ecommerce_db")

# Create 'products' table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    price DECIMAL(10, 2),
    stock INT,
    category VARCHAR(50)
)
""")

# Create 'users' table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
)
""")

# Create 'chat_history' table for storing user chats
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- Auto-incrementing primary key
    user_id INT,                             -- Reference to user ID (foreign key)
    message TEXT,                            -- The chat message
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp of message
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- Foreign key to 'users' table
)
""")


# Generate and insert mock products
products = [generate_product(i) for i in range(1, 101)]
cursor.executemany("""
INSERT INTO products (name, description, price, stock, category) 
VALUES (%s, %s, %s, %s, %s)
""", products)

# Generate and insert mock users
users = [generate_user(i) for i in range(1, 11)]  # Generate 10 mock users
cursor.executemany("""
INSERT INTO users (username, password) 
VALUES (%s, %s)
""", users)

# Generate and insert mock chat history for users
chat_history = [generate_chat(i) for i in range(1, 11)]  # Generate 10 chats for different users
cursor.executemany("""
INSERT INTO chat_history (user_id, message) 
VALUES (%s, %s)
""", chat_history)

# Commit changes and close connection
connection.commit()
connection.close()

print("Database initialized successfully with mock data including products, users, and chat history.")
