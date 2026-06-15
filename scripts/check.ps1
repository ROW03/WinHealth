$ErrorActionPreference = "Stop"

if (Test-Path ".venv\Scripts\Activate.ps1") { . .venv\Scripts\Activate.ps1 }

# Set Python path to the current directory so local modules resolve cleanly
$env:PYTHONPATH = "."

# 1. Ruff Python Linting
ruff check winhealth tests

# 2. Black Code Formatting Check
black --check winhealth tests

# 3. Mypy Type Verification (Using path-based checking)
mypy --strict winhealth/

# 4. Pytest Unit Coverage Bounds
python -m pytest --cov=winhealth --cov-report=term-missing tests/

# 5. Pester PowerShell Tests
if (Test-Path "tests/pester") { Invoke-Pester tests/pester -Passthru }

# 6. ScriptAnalyzer PowerShell Rules
if (Test-Path "collectors") { Invoke-ScriptAnalyzer -Path collectors -Severity Error -EnableExit }