import configparser
import os
import pyodbc


def get_db_connection(target_master: bool = False) -> pyodbc.Connection:
    """Reads config.ini and returns an open connection to the SQL database."""
    config = configparser.ConfigParser()
    config.read("config.ini")

    driver = config.get("database", "Driver", fallback="{ODBC Driver 17 for SQL Server}")
    server = config.get("database", "Server", fallback="localhost\\SQLEXPRESS")
    database = "master" if target_master else config.get("database", "Database", fallback="WinHealth")
    trusted = config.get("database", "Trusted_Connection", fallback="yes")

    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted};"
    return pyodbc.connect(conn_str)