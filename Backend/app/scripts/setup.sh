#!/bin/bash

# Finance & AI Calculator Platform Backend Setup Script

echo "========================================="
echo "Finance Calculator Backend Setup"
echo "========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created (please update with your configuration)"
else
    echo "✓ .env file already exists"
fi

# Initialize database
echo ""
echo "Database Setup:"
echo "1. Update DATABASE_URL in .env file with your PostgreSQL connection string"
echo "2. Run: psql -U postgres -f scripts/init_db.sql"
echo "3. Or manually execute the SQL in your database client"

echo ""
echo "Firebase Setup:"
echo "1. Download your Firebase service account key from Firebase Console"
echo "2. Update FIREBASE_CREDENTIALS_JSON in .env file"

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To run the backend:"
echo "  source venv/bin/activate"
echo "  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "To run tests:"
echo "  pytest app/tests/ -v"
echo ""
