#!/bin/bash
# Git Setup Script for Credit Bills Management System
# Run this script to initialize Git repositories for both backend and frontend

echo "🚀 Setting up Git repositories for Credit Bills Management System..."

# Function to setup git config if not already set
setup_git_config() {
    echo "📝 Configuring Git user identity..."
    
    # Check if git user.name is set
    if [ -z "$(git config --global user.name)" ]; then
        echo "Setting up Git user name..."
        git config --global user.name "Credit Bills Developer"
    fi
    
    # Check if git user.email is set
    if [ -z "$(git config --global user.email)" ]; then
        echo "Setting up Git user email..."
        git config --global user.email "developer@creditbills.com"
    fi
    
    echo "✅ Git configuration complete!"
    echo "User: $(git config --global user.name)"
    echo "Email: $(git config --global user.email)"
}

# Setup global git config
setup_git_config

echo ""
echo "🔧 Setting up Backend Git repository..."
cd backend

# Initialize backend repo if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✅ Backend Git repository initialized"
else
    echo "ℹ️  Backend Git repository already exists"
fi

# Add all files and commit if there are changes
if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "Initial backend setup: Flask API with dynamic header configuration

- Credit bills management with 42+ configurable columns
- SQLAlchemy ORM with PostgreSQL support
- RESTful API endpoints for bills and header config
- Advanced filtering, search, and pagination
- Database migrations with Alembic
- Complete requirements.txt with all dependencies"
    echo "✅ Backend initial commit completed"
else
    echo "ℹ️  Backend repository is up to date"
fi

echo ""
echo "🎨 Setting up Frontend Git repository..."
cd ../frontend

# Initialize frontend repo if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✅ Frontend Git repository initialized"
else
    echo "ℹ️  Frontend Git repository already exists"
fi

# Add all files and commit if there are changes
if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "Initial frontend setup: Angular 20 with backend API integration

- Dynamic table component with backend API integration
- Real-time data loading from Flask API
- Search, pagination, and filtering capabilities
- TypeScript interfaces matching backend models
- Responsive design with mobile support
- Direct API calls without PrimeNG complexity"
    echo "✅ Frontend initial commit completed"
else
    echo "ℹ️  Frontend repository is up to date"
fi

echo ""
echo "📊 Repository Status Summary:"
echo "================================"
cd ../backend
echo "Backend repository:"
echo "  📁 $(pwd)"
echo "  📈 $(git log --oneline | wc -l) commit(s)"
echo "  📦 $(git ls-files | wc -l) tracked files"

cd ../frontend  
echo "Frontend repository:"
echo "  📁 $(pwd)"
echo "  📈 $(git log --oneline | wc -l) commit(s)"
echo "  📦 $(git ls-files | wc -l) tracked files"

echo ""
echo "🎉 Git setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Add remote repositories: git remote add origin <repository-url>"
echo "2. Push to remote: git push -u origin main"
echo "3. Create feature branches: git checkout -b feature/new-feature"
echo "4. Follow conventional commits for future changes"
echo ""
echo "🔗 Useful Git commands:"
echo "  git status          - Check repository status"
echo "  git log --oneline   - View commit history"
echo "  git branch -a       - List all branches"
echo "  git remote -v       - View remote repositories"