import sys
import sqlite3
from collectors import run_powershell_collector
from db import save_snapshot_to_db
import reports
from db import save_snapshot_to_db, purge_old_snapshots
import logging

logging.basicConfig(
    filename="winhealth.log", 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

def init_db():
    conn = sqlite3.connect("WinHealth.db")
    
    # Base table creation
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pc_name TEXT NOT NULL, 
            os_type TEXT NOT NULL, 
            cpu_usage_pct REAL,
            total_ram_gb REAL, 
            free_ram_gb REAL, 
            disk_free_gb REAL, 
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Get a list of columns that currently exist in the database
    cursor = conn.execute("PRAGMA table_info(Snapshots);")
    existing_columns = [row[1] for row in cursor.fetchall()]
    
    # If a column is missing, add it dynamically
    if "total_disk_gb" not in existing_columns:
        conn.execute("ALTER TABLE Snapshots ADD COLUMN total_disk_gb REAL;")
    if "top_process" not in existing_columns:
        conn.execute("ALTER TABLE Snapshots ADD COLUMN top_process TEXT;")
    if "process_working_set_mb" not in existing_columns:
        conn.execute("ALTER TABLE Snapshots ADD COLUMN process_working_set_mb REAL;")

    conn.execute("""
        CREATE VIEW IF NOT EXISTS v_LowDiskAlerts AS
        SELECT pc_name, MIN((disk_free_gb / total_disk_gb) * 100) AS min_free_pct
        FROM Snapshots
        WHERE timestamp >= datetime('now', '-1 day')
        GROUP BY pc_name
        HAVING min_free_pct < 10;
    """)

    conn.close()
    print("Database layout and views are fully initialized and updated.")

def collect_metrics():
    # Grab data from the two external powershell scripts
    system_data = run_powershell_collector("scripts/Get-SystemSnapshot.ps1")
    disk_data = run_powershell_collector("scripts/Get-DiskInventory.ps1")
    
    combined_payload = {**system_data, **disk_data}

    save_snapshot_to_db(combined_payload)
    print("Data collected and saved successfully")

def show_reports_menu():
    print("1. Low Disk Report (Last 24h < 10% Free)")
    print("2. Top 5 Processes by Memory (Last 7 Days)")
    print("3. Hourly CPU Load Profile")
    choice = input("Select a report number (1-3):").strip()
    
    if choice == "1":
        reports.run_low_disk_report()
    elif choice == "2":
        reports.run_top_processes_report()
    elif choice == "3":
        reports.run_hourly_cpu_profile()
    else:
        print("Invalid choice. Please choose 1, 2, or 3.")

def main():
    if len(sys.argv) < 2:
        print("choose: init-db, collect, report or purge")
        user_choice = input("Enter your choice: ").strip().lower()
    else:
        user_choice = sys.argv[1].lower()

    if user_choice == "init-db":
        init_db()
    elif user_choice == "collect":
        collect_metrics()
    elif user_choice == "report":
        show_reports_menu()
    elif user_choice == "purge":
        days_input = input("Enter the number of days to keep snapshots (e.g., 30): ").strip()
        try:
            days = int(days_input)
            deleted = purge_old_snapshots(days)
            logging.info(f"Purged {deleted} snapshots older than {days} days.")
        except ValueError:
            print("Please enter a valid number of days.")
            logging.warning(f"Invalid input for days: {days_input}")
    else:
        print("Invalid choice. Please choose init-db, collect, report or purge.")

if __name__ == "__main__":
    main()
    