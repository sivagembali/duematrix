# Git Setup Script for Credit Bills Management System (PowerShell)
# Run this script to initialize Git repositories for both backend and frontend

Write-Host "🚀 Setting up Git repositories for Credit Bills Management System..." -ForegroundColor Green

# Function to setup git config if not already set
function Setup-GitConfig {
    Write-Host "📝 Configuring Git user identity..." -ForegroundColor Yellow
    
    # Check if git user.name is set
    $userName = git config --global user.name
    if (-not $userName) {
        Write-Host "Setting up Git user name..." -ForegroundColor Cyan
        git config --global user.name "Credit Bills Developer"
    }
    
    # Check if git user.email is set
    $userEmail = git config --global user.email
    if (-not $userEmail) {
        Write-Host "Setting up Git user email..." -ForegroundColor Cyan
        git config --global user.email "developer@creditbills.com"
    }
    
    Write-Host "✅ Git configuration complete!" -ForegroundColor Green
    Write-Host "User: $(git config --global user.name)" -ForegroundColor White
    Write-Host "Email: $(git config --global user.email)" -ForegroundColor White
}

# Setup global git config
Setup-GitConfig

Write-Host ""
Write-Host "🔧 Setting up Backend Git repository..." -ForegroundColor Blue
Set-Location backend

# Initialize backend repo if not already done
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Backend Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Backend Git repository already exists" -ForegroundColor Yellow
}

# Add all files and commit if there are changes
$status = git status --porcelain
if ($status) {
    git add .
    git commit -m "Initial backend setup: Flask API with dynamic header configuration

- Credit bills management with 42+ configurable columns
- SQLAlchemy ORM with PostgreSQL support
- RESTful API endpoints for bills and header config
- Advanced filtering, search, and pagination
- Database migrations with Alembic
- Complete requirements.txt with all dependencies"
    Write-Host "✅ Backend initial commit completed" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Backend repository is up to date" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎨 Setting up Frontend Git repository..." -ForegroundColor Blue
Set-Location ../frontend

# Initialize frontend repo if not already done
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Frontend Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Frontend Git repository already exists" -ForegroundColor Yellow
}

# Add all files and commit if there are changes
$status = git status --porcelain
if ($status) {
    git add .
    git commit -m "Initial frontend setup: Angular 20 with backend API integration

- Dynamic table component with backend API integration
- Real-time data loading from Flask API
- Search, pagination, and filtering capabilities
- TypeScript interfaces matching backend models
- Responsive design with mobile support
- Direct API calls without PrimeNG complexity"
    Write-Host "✅ Frontend initial commit completed" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Frontend repository is up to date" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📊 Repository Status Summary:" -ForegroundColor Magenta
Write-Host "================================" -ForegroundColor Magenta

Set-Location ../backend
$backendCommits = (git log --oneline | Measure-Object).Count
$backendFiles = (git ls-files | Measure-Object).Count
Write-Host "Backend repository:" -ForegroundColor White
Write-Host "  📁 $(Get-Location)" -ForegroundColor Gray
Write-Host "  📈 $backendCommits commit(s)" -ForegroundColor Gray
Write-Host "  📦 $backendFiles tracked files" -ForegroundColor Gray

Set-Location ../frontend
$frontendCommits = (git log --oneline | Measure-Object).Count
$frontendFiles = (git ls-files | Measure-Object).Count
Write-Host "Frontend repository:" -ForegroundColor White
Write-Host "  📁 $(Get-Location)" -ForegroundColor Gray
Write-Host "  📈 $frontendCommits commit(s)" -ForegroundColor Gray
Write-Host "  📦 $frontendFiles tracked files" -ForegroundColor Gray

Write-Host ""
Write-Host "🎉 Git setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "1. Add remote repositories: git remote add origin <repository-url>" -ForegroundColor White
Write-Host "2. Push to remote: git push -u origin main" -ForegroundColor White
Write-Host "3. Create feature branches: git checkout -b feature/new-feature" -ForegroundColor White
Write-Host "4. Follow conventional commits for future changes" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Useful Git commands:" -ForegroundColor Yellow
Write-Host "  git status          - Check repository status" -ForegroundColor White
Write-Host "  git log --oneline   - View commit history" -ForegroundColor White
Write-Host "  git branch -a       - List all branches" -ForegroundColor White
Write-Host "  git remote -v       - View remote repositories" -ForegroundColor White

# Return to root directory
Set-Location ..