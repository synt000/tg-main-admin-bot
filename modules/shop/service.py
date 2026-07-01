# Online Shop Module Business Logic Service Layer
from core.database import get_db_connection

class ShopService:
    @staticmethod
    def create_product(biz_id, name, count, price, barcode=None):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("INSERT INTO products (business_id, product_name, stock_count, price, barcode) VALUES (%s, %s, %s, %s, %s);", (biz_id, name, count, price, barcode))
        conn.commit(); cur.close(); conn.close()
        return True

    @staticmethod
    def update_product_stock(biz_id, prod_id, count):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("UPDATE products SET stock_count = %s WHERE product_id = %s AND business_id = %s;", (count, prod_id, biz_id))
        conn.commit(); cur.close(); conn.close()
        return True

    @staticmethod
    def delete_product(biz_id, prod_id):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE product_id = %s AND business_id = %s;", (prod_id, biz_id))
        conn.commit(); cur.close(); conn.close()
        return True

    @staticmethod
    def list_products(biz_id):
        conn = get_db_connection(); cur = conn.cursor()
        cur.execute("SELECT product_id, product_name, stock_count, price FROM products WHERE business_id = %s;", (biz_id,))
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
# Shop Module Business Logic Service
