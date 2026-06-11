import sqlite3

def get_db_connection():
    return sqlite3.connect("WinHealth.db")

def run_low_disk_report():
    """Hosts with less than 10% disk free in the last 24 hours."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pc_name, MIN((disk_free_gb / total_disk_gb) * 100) 
        FROM Snapshots
        WHERE timestamp >= datetime('now', '-1 day')
        GROUP BY pc_name
        HAVING MIN((disk_free_gb / total_disk_gb) * 100) < 10.0
    """)
    print("\n Low Disk Report (Last 24h < 10% Free)")
    for row in cursor.fetchall():
        print(f"Host: {row[0]} | Min Free %: {row[1]:.2f}%")
    conn.close()

def run_top_processes_report():
    """Top 5 processes by average memory use over the last 7 days."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pc_name, top_process, AVG(process_working_set_mb)
        FROM Snapshots
        WHERE timestamp >= datetime('now', '-7 days') AND top_process IS NOT NULL
        GROUP BY pc_name, top_process
        ORDER BY AVG(process_working_set_mb) DESC
        LIMIT 5
    """)
    print("\n Top 5 Processes by Memory (Last 7 Days)")
    for row in cursor.fetchall():
        print(f"Host: {row[0]} | Process: {row[1]} | Avg Memory: {row[2]:.2f} MB")
    conn.close()

def run_hourly_cpu_profile():
    """Hour-of-day CPU load profile per host (replaces DATEPART)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pc_name, strftime('%H', timestamp), AVG(cpu_usage_pct)
        FROM Snapshots
        GROUP BY pc_name, strftime('%H', timestamp)
        ORDER BY pc_name, strftime('%H', timestamp) ASC
    """)
    print("\n Hourly CPU Load Profile")
    for row in cursor.fetchall():
        print(f"Host: {row[0]} | Hour: {row[1]}:00 | Avg CPU: {row[2]:.2f}%")
    conn.close()