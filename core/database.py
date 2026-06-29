import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)

def init_ecommerce_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        username VARCHAR(255),
        full_name VARCHAR(255),
        balance NUMERIC DEFAULT 0.0,
        commission_earned NUMERIC DEFAULT 0.0,
        role VARCHAR(50) DEFAULT 'user'
    );
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price NUMERIC NOT NULL,
        stock INTEGER DEFAULT 1,
        image_file_id VARCHAR(255),
        category VARCHAR(100)
    );
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        buyer_id BIGINT REFERENCES users(user_id),
        product_id INTEGER REFERENCES products(product_id),
        referred_by BIGINT REFERENCES users(user_id) DEFAULT NULL,
        status VARCHAR(50) DEFAULT 'pending',
        payment_proof VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    init_ecommerce_db()
    print("🛒 Render PostgreSQL E-Commerce DB initialized successfully!")
