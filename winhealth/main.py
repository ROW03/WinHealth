import sqlite3
from collectors import run_powershell_collector
from db import save_snapshot_to_db

conn = sqlite3.connect("WinHealth.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS Snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pc_name TEXT NOT NULL, 
        os_type TEXT NOT NULL, 
        
        cpu_usage_pct REAL CHECK(cpu_usage_pct >= 0 AND cpu_usage_pct <= 100),
        total_ram_gb REAL CHECK(total_ram_gb >= 0), 
        free_ram_gb REAL CHECK(free_ram_gb >= 0),
        disk_free_gb REAL CHECK(disk_free_gb >= 0),
             
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.close()

system_data = run_powershell_collector("scripts/Get-SystemSnapshot.ps1")
disk_data = run_powershell_collector("scripts/Get-DiskInventory.ps1")

combined_payload = {**system_data, **disk_data}

save_snapshot_to_db(combined_payload)
print("SUCCESS, Data pipeline executed. Metrics saved to WinHealth.db")