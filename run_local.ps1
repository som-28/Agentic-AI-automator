# PowerShell helper to run the FastAPI app locally
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Definition)
python -m pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
