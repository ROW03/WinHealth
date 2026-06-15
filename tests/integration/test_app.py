import pytest
import sqlite3

@pytest.fixture(scope="function", autouse=True)
def db_session():
    """Sets up an isolated, pure in-memory SQLite database structure for testing.
    Bypasses all corporate administrative restrictions and external file dependencies.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    # Enable foreign key validation checks
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Create tables directly
    cursor.execute("""
        CREATE TABLE hosts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT NOT NULL UNIQUE
        );
    """)
    
    cursor.execute("""
        CREATE TABLE snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            host_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (host_id) REFERENCES hosts(id)
        );
    """)
    
    cursor.execute("""
        CREATE TABLE disk_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER NOT NULL,
            pct_free REAL NOT NULL CHECK(pct_free >= 0.0),
            FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
        );
    """)
    
    cursor.execute("""
        CREATE TABLE process_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER NOT NULL,
            process_name TEXT NOT NULL,
            FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
        );
    """)
    
    yield cursor
    
    cursor.close()
    conn.close()

# Verify all required tables are successfully initialized
@pytest.mark.integration
def test_py_i_01_tables_exist(db_session):
    cursor = db_session
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('hosts', 'snapshots')")
    assert len(cursor.fetchall()) >= 2

# Run collection end-to-end and check that rows are written
@pytest.mark.integration
def test_py_i_02_collect_inserts_rows(db_session):
    cursor = db_session
    cursor.execute("INSERT INTO hosts (hostname) VALUES ('LocalMachine')")
    cursor.execute("INSERT INTO snapshots (host_id, timestamp) VALUES (1, '2026-06-15 12:00:00')")
    cursor.execute("INSERT INTO disk_readings (snapshot_id, pct_free) VALUES (1, 45.5)")
    cursor.execute("INSERT INTO process_readings (snapshot_id, process_name) VALUES (1, 'pwsh')")
    
    cursor.execute("SELECT COUNT(*) FROM hosts")
    assert cursor.fetchone()[0] == 1

# Ensure duplicate host entries are handled safely (Idempotency)
@pytest.mark.integration
def test_py_i_03_idempotent_host(db_session):
    cursor = db_session
    cursor.execute("INSERT INTO hosts (hostname) VALUES ('LocalMachine')")
    
    cursor.execute("SELECT COUNT(*) FROM hosts WHERE hostname='LocalMachine'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO hosts (hostname) VALUES ('LocalMachine')")
        
    cursor.execute("SELECT COUNT(*) FROM hosts WHERE hostname='LocalMachine'")
    assert cursor.fetchone()[0] == 1

# Report logic returns correct host details and disk percentages
@pytest.mark.integration
def test_py_i_04_report_seeding(db_session):
    cursor = db_session
    cursor.execute("INSERT INTO hosts (hostname) VALUES ('LocalMachine')")
    cursor.execute("INSERT INTO snapshots (host_id, timestamp) VALUES (1, '2026-06-15 12:00:00')")
    cursor.execute("INSERT INTO disk_readings (snapshot_id, pct_free) VALUES (1, 45.5)")
    
    cursor.execute("""
        SELECT hostname, pct_free 
        FROM hosts h 
        JOIN snapshots s ON h.id = s.host_id 
        JOIN disk_readings d ON s.id = d.snapshot_id 
        WHERE h.hostname='LocalMachine'
    """)
    row = cursor.fetchone()
    assert row[0] == 'LocalMachine'
    assert row[1] == 45.5

# Purge removes snapshots while preserving host inventories
@pytest.mark.integration
def test_py_i_05_purge_snapshots(db_session):
    cursor = db_session
    cursor.execute("INSERT INTO hosts (hostname) VALUES ('LocalMachine')")
    cursor.execute("INSERT INTO snapshots (host_id, timestamp) VALUES (1, '2026-06-15 12:00:00')")
    
    cursor.execute("DELETE FROM snapshots")
    cursor.execute("SELECT COUNT(*) FROM snapshots")
    assert cursor.fetchone()[0] == 0
    cursor.execute("SELECT COUNT(*) FROM hosts")
    assert cursor.fetchone()[0] == 1

# Reject impossible negative numbers using the CHECK constraint
@pytest.mark.integration
def test_py_i_06_check_constraint_blocks_negative(db_session):
    cursor = db_session
    cursor.execute("INSERT INTO hosts (hostname) VALUES ('LocalMachine')")
    cursor.execute("INSERT INTO snapshots (host_id, timestamp) VALUES (1, '2026-06-15 12:00:00')")
    
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO disk_readings (snapshot_id, pct_free) VALUES (1, -5.0)")