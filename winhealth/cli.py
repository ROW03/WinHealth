import sys
import sqlite3
from collectors import run_powershell_collector
from db import save_snapshot_to_db

def init_db():
    conn = sqlite3.connect("WinHealth.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pc_name TEXT NOT NULL, 
            os_type TEXT NOT NULL, 
            cpu_usage_pct REAL CHECK(cpu_usage_pct BETWEEN 0.0 AND 100.0),
            total_ram_gb REAL CHECK(total_ram_gb >= 0.0), 
            free_ram_gb REAL CHECK(free_ram_gb >= 0.0), 
            disk_free_gb REAL CHECK(disk_free_gb >= 0.0), 
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.close()
    print("Database is ready")

def collect_metrics():
    # Grab data from the two external powershell scripts
    system_data = run_powershell_collector("scripts/Get-SystemSnapshot.ps1")
    disk_data = run_powershell_collector("scripts/Get-DiskInventory.ps1")
    
    combined_payload = {**system_data, **disk_data}

    save_snapshot_to_db(combined_payload)
    print("Data collected and saved successfully")

def main():
    if len(sys.argv) < 2:
        print("choose: inti-db, collect")
        user_choice = input("Enter your choice: ").strip().lower()
    else:
        user_choice = sys.argv[1].lower()
        
    if user_choice == "init-db":
        init_db()
    elif user_choice == "collect":
        collect_metrics()
    else:
        print("Invalid choice. Please choose 'init-db' or 'collect'.")

if __name__ == "__main__":
    main()
    