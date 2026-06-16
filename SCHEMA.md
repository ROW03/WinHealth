# Database Overview
We use a SQLite database to save system data over time.

## Data Structure
- **SystemMetrics:** Saves the main system status. Every entry gets a unique `snapshot_id`.
- **DiskInventory:** Saves disk space info, linked to the `snapshot_id`.
- **ProcessLogs:** Saves process usage, also linked to the `snapshot_id`.

## Why we use indexes
- **Snapshot_ID:** This is our main link between files, ensuring we can always match data correctly.
- **Timestamp & Name:** We created indexes on these columns so the database can find historical data or specific process info almost instantly.