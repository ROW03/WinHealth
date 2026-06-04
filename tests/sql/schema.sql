IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'winhealth')
BEGIN 
    CREATE DATABASE winhealth;
END
GO

USE tempdb;
GO

IF OBJECT_ID('dbo.Hosts', 'U') IS NULL
BEGIN
    CREATE TABLE Hosts (
        host_id INT IDENTITY(1,1) PRIMARY KEY,
        hostname NVARCHAR(100) NOT NULL UNIQUE,
        os_version NVARCHAR(100) NOT NULL,
        first_seen_utc DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        last_seen_utc DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
    );
END
GO

IF OBJECT_ID('dbo.Snapshots', 'U') IS NULL
BEGIN
    CREATE TABLE Snapshots (
        Snapshots_id INT IDENTITY(1,1) PRIMARY KEY,
        host_id INT NOT NULL,
        captured_utc DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
        uptime_seconds INT NOT NULL,          
        cpu_load_pct INT NOT NULL,
        memory_total_mb INT NOT NULL,        
        memory_free_mb INT NOT NULL,         
        CONSTRAINT FK_Snapshots_Hosts FOREIGN KEY (host_id) REFERENCES Hosts(host_id) 
        ON DELETE CASCADE
    );
END
GO

IF OBJECT_ID('dbo.DiskReadings', 'U') IS NULL
BEGIN
    CREATE TABLE DiskReadings (
        reading_id INT IDENTITY(1,1) PRIMARY KEY,
        snapshot_id INT NOT NULL,
        drive_letter NVARCHAR(10) NOT NULL,    
        total_gb FLOAT NOT NULL,                
        free_gb FLOAT NOT NULL,                 
        pct_free FLOAT NOT NULL,                
        CONSTRAINT FK_DiskReadings_Snapshots FOREIGN KEY (snapshot_id) REFERENCES Snapshots(Snapshots_id) 
        ON DELETE CASCADE
    );
END
GO

IF OBJECT_ID('dbo.ProcessReadings', 'U') IS NULL
BEGIN
    CREATE TABLE ProcessReadings (
        reading_id INT IDENTITY(1,1) PRIMARY KEY,
        snapshot_id INT NOT NULL,
        pid INT NOT NULL,
        process_name NVARCHAR(255) NOT NULL,
        working_set_mb FLOAT NOT NULL,       
        cpu_seconds FLOAT NOT NULL,
        CONSTRAINT FK_ProcessReadings_Snapshots FOREIGN KEY (snapshot_id) REFERENCES Snapshots(Snapshots_id) 
        ON DELETE CASCADE
    );
END
GO