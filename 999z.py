import mysql.connector
from mysql.connector import Error

try:
    db = mysql.connector.connect(
        user="deva",
        password="deva",
        host="127.0.0.1"
    )

    if db.is_connected():
        print("✅ Connected to MySQL Server")
except Error as e:
    print(f"❌ Error: {e}")
finally:
    if 'db' in locals() and db.is_connected():
        db.close()
        print("🔒 Connection closed")
