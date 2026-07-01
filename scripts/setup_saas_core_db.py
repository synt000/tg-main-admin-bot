import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.database import get_db_connection

def build_enterprise_schema():
    print("🚀 Initializing Master PostgreSQL Core Database Engine V2...")
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 🚀 🔒 [MIGRATION ACTIVE]: အစ်ကို ညွှန်ကြားထားသည့် audit_logs ဇယားသစ်အား စနစ်တကျ ထည့်သွင်းခြင်း
    queries = [
        "CREATE TABLE IF NOT EXISTS users (telegram_id BIGINT PRIMARY KEY, username VARCHAR(255), full_name VARCHAR(255), role VARCHAR(50) DEFAULT 'customer', saved_phone VARCHAR(50), saved_address TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS tenants (tenant_id SERIAL PRIMARY KEY, owner_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE, shop_name VARCHAR(255), business_type VARCHAR(100), subscription_status VARCHAR(50) DEFAULT 'active', bot_token VARCHAR(255) UNIQUE, shop_logo_url TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS licenses (license_key VARCHAR(100) PRIMARY KEY, merchant_id VARCHAR(50), key_type VARCHAR(50) DEFAULT 'trial', is_activated BOOLEAN DEFAULT FALSE, expires_at TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS customers (customer_id SERIAL PRIMARY KEY, business_id VARCHAR(50), name VARCHAR(100), phone VARCHAR(30) UNIQUE, total_spent NUMERIC DEFAULT 0, loyalty_points INT DEFAULT 0, tier VARCHAR(20) DEFAULT 'Regular', created_at TIMESTAMP DEFAULT NOW());",
        "CREATE TABLE IF NOT EXISTS customer_activity (id SERIAL PRIMARY KEY, customer_id INT, business_id VARCHAR(50), module VARCHAR(30), action VARCHAR(50), amount NUMERIC DEFAULT 0, created_at TIMESTAMP DEFAULT NOW());",
        "CREATE INDEX IF NOT EXISTS idx_customer_activity_customer_id ON customer_activity(customer_id);",
        "CREATE TABLE IF NOT EXISTS products (product_id SERIAL PRIMARY KEY, business_id VARCHAR(50), product_name VARCHAR(100), stock_count INT DEFAULT 0, price DECIMAL(15,2) DEFAULT 0.00, barcode VARCHAR(100));",
        "CREATE TABLE IF NOT EXISTS orders (order_id VARCHAR(50) PRIMARY KEY, business_id VARCHAR(50), customer_id INT, total_amount DECIMAL(15,2), delivery_status VARCHAR(50) DEFAULT 'Pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS income (income_id SERIAL PRIMARY KEY, business_id VARCHAR(50), amount DECIMAL(15,2), details TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS subscriptions (id SERIAL PRIMARY KEY, business_id VARCHAR(50), plan VARCHAR(20), status VARCHAR(20), provider VARCHAR(30), payment_reference VARCHAR(100) UNIQUE, start_date TIMESTAMP DEFAULT NOW(), end_date TIMESTAMP);",
        "CREATE TABLE IF NOT EXISTS payment_transactions (id SERIAL PRIMARY KEY, business_id VARCHAR(50), provider VARCHAR(30), amount NUMERIC DEFAULT 0, currency VARCHAR(10) DEFAULT 'MMK', status VARCHAR(20), transaction_reference VARCHAR(100) UNIQUE, created_at TIMESTAMP DEFAULT NOW());",
        "CREATE TABLE IF NOT EXISTS telegram_alerts (id SERIAL PRIMARY KEY, business_id VARCHAR(50), alert_type VARCHAR(50), message TEXT, is_resolved BOOLEAN DEFAULT FALSE, created_at TIMESTAMP DEFAULT NOW());",
        # 👑 [AUDIT LOG ENGINE]: အစ်ကို ချမှတ်ပေးလိုက်သော SQL Script အား အသန့်စက်စက် Run ခြင်း
        """
        CREATE TABLE IF NOT EXISTS audit_logs (
            audit_id SERIAL PRIMARY KEY,
            business_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    ]
    
    for q in queries: 
        cur.execute(q)
        
    conn.commit()
    cur.close()
    conn.close()
    print("📊 [SUCCESS]: 15 Master Enterprise Core Database Tables (with Audit Logs) Built Perfectly!")

if __name__ == "__main__": 
    build_enterprise_schema()
