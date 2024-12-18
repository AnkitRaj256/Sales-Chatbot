from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import MySQLdb

# Initialize Flask App
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])  # Allow credentials for cookies and restrict CORS to frontend

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "your_secret_key_here"  # Replace with a strong secret key
app.config['JWT_TOKEN_LOCATION'] = ['cookies']  # Store JWT in cookies
app.config['JWT_COOKIE_SECURE'] = False  # Set to True if running on HTTPS
jwt = JWTManager(app)

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",  # Your MySQL username
    "password": "Ankit@SQL25",  # Your MySQL password
    "database": "ecommerce_db"  # Your database name
}

# Utility function to connect to the database
def get_db_connection():
    try:
        connection = MySQLdb.connect(**DB_CONFIG)
        return connection
    except MySQLdb.Error as e:
        print(f"Database connection error: {e}")
        raise

# --- SIGNUP ROUTE (REGISTER NEW USERS) ---
@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Get username and password from request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Connect to database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"error": "Username already exists"}), 409

        # Insert new user into database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        connection.close()

# --- LOGIN ROUTE ---
@app.route('/login', methods=['POST'])
def login():
    try:
        # Get username and password from request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Connect to database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Validate user credentials (assuming a 'users' table with 'username' and 'password')
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            # Create a JWT token
            access_token = create_access_token(identity=username)
            response = jsonify({"message": "Login successful"})
            response.set_cookie('access_token_cookie', access_token, httponly=True)  # Secure HTTP-only cookie
            return response, 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        connection.close()

# --- LOGOUT ROUTE ---
@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logged out successfully"})
    response.delete_cookie('access_token_cookie')
    return response, 200

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the incoming JSON data
        data = request.get_json()

        if data is None:  # Check if the incoming request body is not JSON
            return jsonify({"error": "Invalid JSON format"}), 400

        query = data.get('query', '').lower()  # Convert query to lowercase for case-insensitive comparison
        
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Search for matching products in the database
        cursor.execute("SELECT * FROM products WHERE LOWER(name) LIKE %s", ('%' + query + '%',))
        matching_products = cursor.fetchall()
        
        # Prepare the response
        if matching_products:
            product_list = '\n'.join([f"{product[1]} ({product[3]})" for product in matching_products])  # Assuming name is at index 1 and price at index 3
            response = {
                "reply": f"Found {len(matching_products)} product(s) matching your query.",
                "product_details": product_list,  # Detailed list of products
                "total_products": len(matching_products),  # Total number of matching products
                "products": [{"id": product[0], "name": product[1], "price": product[3], "category": product[5]} for product in matching_products]  # List of matching products with details
            }
            return jsonify(response), 200
        else:
            # Return a response when no products match
            response = {
                "reply": "No products found matching your query.",
                "total_products": 0,  # Total number of matching products
                "products": []
            }
            return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        # Ensure the database connection is closed
        cursor.close()
        connection.close()





# --- ROOT ROUTE ---
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Flask API!"})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
