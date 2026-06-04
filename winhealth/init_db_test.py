from winhealth.db import get_db_connection

print("Checking winhealth database connection")
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DB_NAME();")
    db_name = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    
    print(f"[SUCCESS] Connected successfully to database: {db_name}")
except Exception as e:
    print(f"\n[ERROR] Connection failed: {e}")