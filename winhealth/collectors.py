import json
import subprocess

# a function that will run whatever powershell script we give it and return the output as JSON
def run_powershell_collector(script_path):
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], 
        capture_output=True, 
        text=True,
        check=True
    )
    return json.loads(result.stdout)