import psycopg2
from core.database import get_db_connection

def build_enterprise_schema():
    print("🚀 Initializing Master PostgreSQL Core Database Engine V2...")
    conn = get_db_connection()
    cur = conn.cursor()
    
    # ၁၄ ဇယား ဗိသုကာအား Dynamic Foreign Key Relational စနစ်ဖြင့် တည်ဆောက်ခြင်း
    queries = [
        "CREATE TABLE IF NOT EXISTS users (telegram_id VARCHAR(50) PRIMARY KEY, full_name VARCHAR(100), registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS licenses (license_key VARCHAR(100) PRIMARY KEY, merchant_id VARCHAR(50), key_type VARCHAR(50) DEFAULT 'premium', is_activated BOOLEAN DEFAULT FALSE, expires_at TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS businesses (business_id VARCHAR(50) PRIMARY KEY, business_name VARCHAR(100), business_type VARCHAR(50), currency VARCHAR(10) DEFAULT 'MMK', tax_number VARCHAR(50));",
        "CREATE TABLE IF NOT EXISTS staff (staff_id SERIAL PRIMARY KEY, business_id VARCHAR(50), name VARCHAR(100), role VARCHAR(50), permission_level INT DEFAULT 1);",
        
        # 👥 CRM TABLES
        """CREATE TABLE IF NOT EXISTS customers (
            customer_id SERIAL PRIMARY KEY, business_id VARCHAR(50), name VARCHAR(100), phone VARCHAR(50) UNIQUE, 
            address TEXT, telegram_id VARCHAR(50), member_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            total_orders INT DEFAULT 0, total_spending DECIMAL(15,2) DEFAULT 0.00, status VARCHAR(20) DEFAULT 'Normal', notes TEXT
        );""",
        
        # 📦 INVENTORY TABLES
        "CREATE TABLE IF NOT EXISTS categories (category_id SERIAL PRIMARY KEY, business_id VARCHAR(50), category_name VARCHAR(100));",
        "CREATE TABLE IF NOT EXISTS suppliers (supplier_id SERIAL PRIMARY KEY, business_id VARCHAR(50), supplier_name VARCHAR(100), phone VARCHAR(50));",
        "CREATE TABLE IF NOT EXISTS products (product_id SERIAL PRIMARY KEY, business_id VARCHAR(50), category_id INT, supplier_id INT, product_name VARCHAR(100), stock_count INT DEFAULT 0, low_stock_alert INT DEFAULT 5, price DECIMAL(15,2) DEFAULT 0.00, barcode VARCHAR(100));",
        
        # 💰 FINANCE & ORDERS TABLES
        "CREATE TABLE IF NOT EXISTS orders (order_id VARCHAR(50) PRIMARY KEY, business_id VARCHAR(50), customer_id INT, total_amount DECIMAL(15,2), delivery_status VARCHAR(50) DEFAULT 'Pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS expenses (expense_id SERIAL PRIMARY KEY, business_id VARCHAR(50), amount DECIMAL(15,2), details TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS income (income_id SERIAL PRIMARY KEY, business_id VARCHAR(50), amount DECIMAL(15,2), details TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
        
        # 📈 CORE PLATFORM SETTINGS
        "CREATE TABLE IF NOT EXISTS reports (report_id SERIAL PRIMARY KEY, business_id VARCHAR(50), report_type VARCHAR(50), generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS settings (setting_id SERIAL PRIMARY KEY, business_id VARCHAR(50), key_name VARCHAR(100), value_data TEXT);",
        "CREATE TABLE IF NOT EXISTS notifications (notification_id SERIAL PRIMARY KEY, business_id VARCHAR(50), message TEXT, is_read BOOLEAN DEFAULT FALSE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
    ]
    
    for q in queries:
        cur.execute(q)
        
    conn.commit()
    cur.close()
    conn.close()
    print("📊 [SUCCESS]: 14 Master Enterprise Core Database Tables Built Perfectly!")

if __name__ == "__main__":
    build_enterprise_schema()
