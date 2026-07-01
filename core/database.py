import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
_db_pool = None

def init_connection_pool():
    global _db_pool
    if _db_pool is None and DATABASE_URL:
        # 🚀 🔒 [SSL ENFORCED POOLING ACTIVE]: အစ်ကို ညွှန်ကြားထားသည့်အတိုင်း TLS စံနှုန်းဖြင့် ဒေတာဘေ့စ် Pool ကြိုဆောက်ခြင်း
        print("🔌 [Database Engine]: Initializing Global Multi-Tenant Connection Pool...")
        _db_pool = SimpleConnectionPool(
            1, 
            20, 
            DATABASE_URL,
            sslmode="require"
        )

def get_db_connection():
    init_connection_pool()
    if _db_pool:
        return _db_pool.getconn()
    
    # 🛡️ 🚀 [LOCAL FALLBACK SSL HARDENING]: Local တောင်းဆိုမှုများကိုပါ SSL Handshake အသေချုပ်ပိတ်ခြင်း
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432"),
        sslmode="require"
    )

def release_db_connection(conn):
    global _db_pool
    if _db_pool and conn:
        _db_pool.putconn(conn)

def get_db_cursor():
    conn = get_db_connection()
    return conn.cursor(cursor_factory=RealDictCursor)
