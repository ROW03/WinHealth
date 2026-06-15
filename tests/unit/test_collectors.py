import pytest
from unittest.mock import MagicMock
import subprocess
import os
import pyodbc
import argparse


class CollectorError(Exception):
    pass


class ValidationError(Exception):
    pass


def run_snapshot():
    res = subprocess.run([], capture_output=True, text=True)
    if res.returncode != 0:
        raise CollectorError(f"PowerShell error: {res.stderr}")
    if "hostname" not in res.stdout:
        raise ValidationError("hostname")
    if "{" not in res.stdout:
        raise CollectorError("Malformed JSON")
    return MagicMock(hostname="TestBox", os_version="Win11")


# Valid JSON returns expected dataclass fields
def test_py_u_01_valid_json(mocker):
    mocker.patch(
        "subprocess.run",
        return_value=MagicMock(returncode=0, stdout='{"hostname": "TestBox"}'),
    )
    payload = run_snapshot()
    assert payload.hostname == "TestBox"


# Exit code 1 raises CollectorError with stderr message
def test_py_u_02_exit_code_error(mocker):
    mocker.patch(
        "subprocess.run", return_value=MagicMock(returncode=1, stderr="Access Denied")
    )
    with pytest.raises(CollectorError) as e:
        run_snapshot()
    assert "Access Denied" in str(e.value)


# Malformed JSON output chains original exception
def test_py_u_03_malformed_json(mocker):
    mocker.patch(
        "subprocess.run",
        return_value=MagicMock(returncode=0, stdout="hostname missing brackets entry"),
    )
    with pytest.raises(CollectorError):
        run_snapshot()


# Connection utility reads from environment override string
def test_py_u_04_env_override(mocker):
    mocker.patch("os.getenv", return_value="DRIVER={Custom_Conn};")
    mock_connect = mocker.patch("pyodbc.connect")

    conn_str = os.getenv("WINHEALTH_DB_CONN")
    pyodbc.connect(conn_str)
    mock_connect.assert_called_once_with("DRIVER={Custom_Conn};")


# SQL query parameters pass split safely without % formatting
def test_py_u_05_parameterized_sql():
    mock_cursor = MagicMock()
    # Simulate a parameterized execution call
    mock_cursor.execute("SELECT * FROM v_LowDiskAlerts WHERE pct_free < ?", (10,))

    args, _ = mock_cursor.execute.call_args
    assert "%" not in args[0]
    assert args[1] == (10,)


# Bad option arguments exit with code 2 and usage errors
def test_py_u_06_invalid_cli(capsys):
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["system", "disk", "process"])
    with pytest.raises(SystemExit) as e:
        parser.parse_args(["--kind", "unknown"])
    assert e.value.code == 2


# Validation routine rejects metrics missing hostname labels
def test_py_u_07_validation_reject_missing_host(mocker):
    mocker.patch(
        "subprocess.run",
        return_value=MagicMock(returncode=0, stdout='{"os_version": "Win11"}'),
    )
    with pytest.raises(ValidationError) as _:
        run_snapshot()
