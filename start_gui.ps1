# Quick Start Script for Personal Task Automation Agent GUI

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Personal Task Automation Agent - GUI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.10+ first." -ForegroundColor Red
    exit 1
}

# Check if requirements are installed
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow

$requiredPackages = @("streamlit", "fastapi", "PyPDF2", "python-docx")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    $installed = python -c "import $($package.ToLower().Replace('-', '_'))" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-Host "⚠️  Missing packages detected: $($missingPackages -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    $install = Read-Host "Install missing packages? (Y/n)"
    
    if ($install -ne 'n' -and $install -ne 'N') {
        Write-Host "Installing dependencies..." -ForegroundColor Yellow
        pip install -r requirements.txt
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
            exit 1
        }
    }
} else {
    Write-Host "✓ All dependencies installed" -ForegroundColor Green
}

# Check .env file
Write-Host ""
if (Test-Path ".env") {
    Write-Host "✓ Configuration file (.env) found" -ForegroundColor Green
    
    # Check for API keys
    $envContent = Get-Content ".env" -Raw
    
    if ($envContent -match "SERPAPI_KEY=.+") {
        Write-Host "  ✓ SerpAPI key configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  SerpAPI key not configured (will use demo mode)" -ForegroundColor Yellow
    }
    
    if ($envContent -match "OPENAI_API_KEY=.+") {
        Write-Host "  ✓ OpenAI key configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  OpenAI key not configured (will use fallback)" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  No .env file found (will use defaults)" -ForegroundColor Yellow
    Write-Host "  Create .env file from .env.example for API configuration" -ForegroundColor Yellow
}

# Show features
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Available Features:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  📋 Task Execution - Natural language commands" -ForegroundColor White
Write-Host "  📄 Resume Analysis - Upload & analyze resumes" -ForegroundColor White
Write-Host "  💼 Job Matching - Find jobs based on resume" -ForegroundColor White
Write-Host "  📜 History - Track all executions" -ForegroundColor White
Write-Host ""

# Offer to run test
Write-Host "Would you like to:" -ForegroundColor Yellow
Write-Host "  1. Start GUI (recommended)" -ForegroundColor White
Write-Host "  2. Run resume workflow test" -ForegroundColor White
Write-Host "  3. Run agent test" -ForegroundColor White
Write-Host "  4. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "Starting Streamlit GUI..." -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "The GUI will open in your browser at:" -ForegroundColor Yellow
        Write-Host "  http://localhost:8501" -ForegroundColor Green
        Write-Host ""
        Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
        Write-Host ""
        
        streamlit run src/app_gui.py
    }
    "2" {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "Running Resume Workflow Test..." -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        
        python test_resume_workflow.py
        
        Write-Host ""
        Write-Host "Press Enter to continue..." -ForegroundColor Yellow
        Read-Host
    }
    "3" {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "Running Agent Test..." -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        
        python test_agent_enhanced.py
        
        Write-Host ""
        Write-Host "Press Enter to continue..." -ForegroundColor Yellow
        Read-Host
    }
    default {
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit 0
    }
}
