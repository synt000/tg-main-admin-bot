cur.execute("""
CREATE TABLE IF NOT EXISTS vip_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    plan TEXT,
    expires_at TEXT,
    status TEXT DEFAULT 'active'
)
""")
