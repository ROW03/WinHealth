import sqlite3
from collectors import run_powershell_collector
from db import save_snapshot_to_db

conn = sqlite3.connect("WinHealth.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS Snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pc_name TEXT, os_type TEXT, cpu_usage_pct REAL,
        total_ram_gb REAL, free_ram_gb REAL, disk_free_gb REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.close()

system_data = run_powershell_collector("scripts/Get-SystemSnapshot.ps1")
disk_data = run_powershell_collector("scripts/Get-DiskInventory.ps1")

combined_payload = {**system_data, **disk_data}

save_snapshot_to_db(combined_payload)
print("SUCCESS, Data pipeline executed. Metrics saved to WinHealth.db")