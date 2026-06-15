import json
import subprocess
from typing import Any


class CollectorError(Exception):
    """Custom exception for collector errors."""

    pass


# a function that will run whatever powershell script we give it and return the output as JSON
def run_powershell_collector(script_path: str) -> Any:
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
        capture_output=True,
        text=True,
    )
    # if window blocks/crashes the script, we want to catch that and raise a custom error
    if result.returncode != 0:
        raise CollectorError(f"Script failed: {script_path}: {result.stderr.strip()}")

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise CollectorError(
            f"Script {script_path} didn't return valid JSON: {result.stdout.strip()}"
        )
