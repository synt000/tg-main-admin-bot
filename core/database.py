import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    # Production Level အတွက် Database URL နှင့် တိုက်ရိုက်ချိတ်ဆက်ခြင်း
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    return conn

def init_saas_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # ၁။ Users Table (SaaS Account Roles & Checkout Memory စနစ်ပါဝင်သည်)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        telegram_id BIGINT PRIMARY KEY,
        username VARCHAR(255),
        full_name VARCHAR(255),
        role VARCHAR(50) NOT NULL DEFAULT 'customer', -- super_admin, shop_owner, customer
        saved_phone VARCHAR(50),                      -- One-Click Checkout အတွက် ဖုန်း
        saved_address TEXT,                           -- One-Click Checkout အတွက် လိပ်စာ
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    # ၂။ Tenants Table (Whitelabel ဆိုင်ရှင်များစာရင်းနှင့် Subscription Status)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tenants (
        tenant_id SERIAL PRIMARY KEY,
        owner_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
        shop_name VARCHAR(255) NOT NULL,
        business_type VARCHAR(100) NOT NULL,          -- ecommerce, booking, fnb
        subscription_status VARCHAR(50) DEFAULT 'active', -- active, suspended, expired
        bot_token VARCHAR(255) NOT NULL UNIQUE,       -- Whitelabel Self-Onboarding Token
        shop_logo_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    # ၃။ Products Table (ဘက်စုံသုံး ပစ္စည်းစာရင်း - Stock ကန့်သတ်ချက်နှင့် Add-on Options JSONB ပါဝင်သည်)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        tenant_id INTEGER REFERENCES tenants(tenant_id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price NUMERIC(12,2) NOT NULL,
        image_url TEXT,
        category VARCHAR(100),
        stock_quantity INTEGER DEFAULT -1,            -- -1 ဆိုလျှင် ကန့်သတ်ချက်မရှိ (Infinite)
        add_on_options JSONB DEFAULT '[]',            -- Layout C (F&B) Add-on Pop-up အတွက်
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    # ၄။ Booking Slots Table (Layout B Booking ပြက္ခဒိန် အချိန်အပိုင်းအခြားစနစ်အတွက်)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS booking_slots (
        slot_id SERIAL PRIMARY KEY,
        tenant_id INTEGER REFERENCES tenants(tenant_id) ON DELETE CASCADE,
        product_id INTEGER REFERENCES products(product_id) ON DELETE CASCADE,
        available_date DATE NOT NULL,
        time_start TIME NOT NULL,
        time_end TIME NOT NULL,
        is_booked BOOLEAN DEFAULT FALSE
    );
    ''')
    
    # ၅။ Orders Table (TMA Orders, Digital Voucher & OCR Scan Data သိမ်းဆည်းရန်)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        tenant_id INTEGER REFERENCES tenants(tenant_id) ON DELETE CASCADE,
        customer_id BIGINT REFERENCES users(telegram_id),
        total_amount NUMERIC(12,2) NOT NULL,
        order_type VARCHAR(50),                       -- ecommerce, booking, fnb
        payment_status VARCHAR(50) DEFAULT 'pending',  -- pending, paid, verified
        payment_proof_url TEXT,                       -- OCR / Screenshot သိမ်းရန် လင့်ခ်
        qr_voucher_code VARCHAR(100) UNIQUE,          -- Download ဆွဲနိုင်မည့် Auto Digital Voucher Code
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    # ၆။ Subscription Logs Table (Super Admin မှ လစဉ်ကြေး သက်တမ်း စီမံခန့်ခွဲရန်)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscription_logs (
        log_id SERIAL PRIMARY KEY,
        tenant_id INTEGER REFERENCES tenants(tenant_id) ON DELETE CASCADE,
        amount_paid NUMERIC(12,2) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    # ၇။ External Omnichannel Orders Table (Facebook / TikTok Shop Sync အော်ဒါများ)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS external_orders (
        ext_order_id SERIAL PRIMARY KEY,
        tenant_id INTEGER REFERENCES tenants(tenant_id) ON DELETE CASCADE,
        platform VARCHAR(50) NOT NULL,                -- facebook, tiktok
        platform_order_id VARCHAR(255) NOT NULL,
        customer_name VARCHAR(255),
        items_summary JSONB NOT NULL,
        total_price NUMERIC(12,2) NOT NULL,
        synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')
    
    # 🛡️ POSTGRESQL ROW-LEVEL SECURITY (RLS) ENABLE ပြုလုပ်ခြင်း
    cursor.execute("ALTER TABLE products ENABLE ROW LEVEL SECURITY;")
    cursor.execute("ALTER TABLE orders ENABLE ROW LEVEL SECURITY;")
    
    # Tenants Isolation Policy ဖန်တီးခြင်း (ဆိုင်ရှင်အချင်းချင်း ဒေတာကျော်မမြင်နိုင်စေရန်)
    cursor.execute('''
    DO $$ 
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'tenant_isolation_policy') THEN
            CREATE POLICY tenant_isolation_policy ON products 
            USING (tenant_id = current_setting('app.current_tenant_id', true)::INTEGER);
        END IF;
    END $$;
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    # Local သို့မဟုတ် Server ပေါ်တွင် တိုက်ရိုက် စမ်းသပ်ရန်
    init_saas_database()
    print("🚀 SaaS Multi-Tenant Database with RLS Security initialized successfully!")
