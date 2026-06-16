# WinHealth Suite
A robust, automated suite for gathering Windows system telemetry, disk inventory, and process performance data.

## Prerequisites
- Windows 10/11 
- PowerShell 7.2+
- Python 3.14+ 
- Virtual Environment (`.venv`) initialized in the root directory

## Install Steps
1. Clone the repository to your local machine.
2. Initialize the virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt