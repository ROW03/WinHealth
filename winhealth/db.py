import sqlite3

def save_snapshot_to_db(payload):
    # Connect to a local file database 
    conn = sqlite3.connect("WinHealth.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO Snapshots (pc_name, os_type, cpu_usage_pct, total_ram_gb, free_ram_gb, disk_free_gb)
        values (?, ?, ?, ?, ?, ?);
        """,
        (
            payload("pc_name"),
            payload("os_type"),
            payload("cpu_usage_pct"),
            payload("total_ram_gb"),
            payload("free_ram_gb"),
            payload("disk_free_gb")
        )
    )
    conn.commit()
    conn.close()