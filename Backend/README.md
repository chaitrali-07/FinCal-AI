# Finance & AI Calculator Platform Backend

Production-grade financial calculator backend built with FastAPI, PostgreSQL, and Firebase authentication.

## Overview

This backend provides:
- **20+ Deterministic Financial Calculators** - EMI, SIP, CAGR, FD, RD, Tax (Old/New Regime), Retirement Planning, etc.
- **Firebase Authentication** - Secure JWT token verification
- **Audit Trail** - Complete calculation history storage
- **User Profiles** - Track user calculations and templates
- **REST API** - Well-documented endpoints with Swagger UI

## Project Structure

```
backend/
├── app/
│   ├── calculators/          # Pure calculation functions
│   │   ├── emi.py
│   │   ├── sip.py
│   │   ├── cagr.py
│   │   ├── fd.py
│   │   ├── rd.py
│   │   ├── tax.py
│   │   └── other.py
│   │
│   ├── routers/              # FastAPI route handlers
│   │   ├── loan.py
│   │   ├── investment.py
│   │   ├── tax.py
│   │   └── other.py
│   │
│   ├── schemas/              # Pydantic validation schemas
│   │   ├── loan_schema.py
│   │   ├── investment_schema.py
│   │   ├── tax_schema.py
│   │   └── other_schema.py
│   │
│   ├── db/                   # Database models and connection
│   │   ├── models.py
│   │   └── database.py
│   │
│   ├── services/             # Business logic services
│   │   ├── auth.py
│   │   └── calculator_router.py
│   │
│   ├── tests/                # Unit tests
│   │   └── test_calculators.py
│   │
│   └── main.py               # FastAPI app entry point
│
├── scripts/                  # Setup and migration scripts
│   ├── init_db.sql
│   └── setup.sh
│
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip or poetry

### Setup Steps

1. **Clone and enter directory**
   ```bash
   cd backend
   ```

2. **Run setup script**
   ```bash
   bash scripts/setup.sh
   ```

   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database**
   ```bash
   psql -U postgres -f scripts/init_db.sql
   # Or use your database client to execute init_db.sql
   ```

5. **Setup Firebase (Optional)**
   - Download service account key from Firebase Console
   - Set `FIREBASE_CREDENTIALS_JSON` path in `.env`

## Configuration

### Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/finance_calc

# Firebase
FIREBASE_CREDENTIALS_JSON=/path/to/firebase-key.json

# API
HOST=0.0.0.0
PORT=8000
RELOAD=False

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# App
ENVIRONMENT=development
DEBUG=False
```

## Running the Backend

### Development
```bash
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

### Access Swagger UI
Navigate to `http://localhost:8000/api/docs`

### Available Calculators

#### Loan Calculators
- `POST /api/calculate/loan/emi` - EMI Calculator
- `POST /api/calculate/loan/emi-for-payment` - Reverse EMI (tenure for given EMI)

#### Investment Calculators
- `POST /api/calculate/investment/sip` - SIP Calculator
- `POST /api/calculate/investment/lumpsum` - Lumpsum Investment
- `POST /api/calculate/investment/cagr` - CAGR Calculator
- `POST /api/calculate/investment/required-return` - Required Return
- `POST /api/calculate/investment/fd` - Fixed Deposit
- `POST /api/calculate/investment/rd` - Recurring Deposit
- `POST /api/calculate/investment/rd-simple` - RD (Simplified Method)

#### Tax Calculators
- `POST /api/calculate/tax/old-regime` - Income Tax (Old Regime)
- `POST /api/calculate/tax/new-regime` - Income Tax (New Regime)
- `POST /api/calculate/tax/compare-regimes` - Tax Regime Comparison

#### Other Calculators
- `POST /api/calculate/other/inflation-adjusted` - Inflation Adjustment
- `POST /api/calculate/other/future-value-inflation` - Future Value with Inflation
- `POST /api/calculate/other/retirement-corpus` - Retirement Corpus
- `POST /api/calculate/other/retirement-corpus-with-savings` - Retirement with Savings

### Example Request

```bash
curl -X POST "http://localhost:8000/api/calculate/loan/emi" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -d '{
    "principal": 500000,
    "interest_rate": 9.5,
    "tenure_months": 60
  }'
```

### Example Response

```json
{
  "result": {
    "emi": 10487.32,
    "total_payment": 629239.20,
    "total_interest": 129239.20,
    "principal": 500000
  },
  "assumptions": {
    "interest_compounding": "monthly",
    "payment_frequency": "monthly",
    "interest_calculation": "reducing balance"
  },
  "formula": "EMI = P × r × (1+r)^n / ((1+r)^n − 1)",
  "calculator_version": "1.0",
  "inputs": {
    "principal": 500000,
    "annual_interest_rate": 9.5,
    "tenure_months": 60
  }
}
```

## Running Tests

```bash
# All tests
pytest app/tests/ -v

# Specific test file
pytest app/tests/test_calculators.py -v

# With coverage
pytest app/tests/ --cov=app --cov-report=html
```

## Database Schema

### Users Table
Stores user information from Firebase auth

### CalculationHistory Table
Audit trail of all calculations performed by users
- user_id: Firebase UID
- calculator_type: Type of calculation
- inputs: Input parameters (JSON)
- result: Calculation result (JSON)
- created_at: Timestamp

### CalculationTemplates Table
User-saved templates for quick access

### QuickNotes Table
User notes and insights related to calculations

## Architecture Decisions

### Pure Functions
All calculators are pure functions with no side effects:
- No database queries inside calculator functions
- Deterministic - same inputs always produce same outputs
- Fully testable in isolation
- Easy to version and maintain

### Separation of Concerns
- **Calculators**: Pure math
- **Routes**: HTTP handling
- **Schemas**: Input/output validation
- **Services**: Auth and routing logic
- **DB**: Persistence layer

### Security
- Firebase JWT token verification
- CORS configuration
- Input validation with Pydantic
- SQL parameterized queries (via SQLAlchemy)

## Production Deployment

### Using Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

### Using Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup
- Use environment variables for sensitive data
- Set `ENVIRONMENT=production`
- Disable `DEBUG=False`
- Use production database
- Configure proper CORS origins

## Troubleshooting

### Database Connection Error
```
Check DATABASE_URL in .env
Verify PostgreSQL is running
Ensure database exists and user has permissions
```

### Firebase Token Error
```
Verify FIREBASE_CREDENTIALS_JSON path
Check Firebase project credentials are valid
Ensure token is not expired
```

### Port Already in Use
```bash
lsof -i :8000  # Find process using port
kill -9 <PID>  # Kill the process
```

## Performance Optimization

- Connection pooling (QueuePool with 10 size, 20 overflow)
- Index on frequently queried columns
- Async/await for I/O operations
- Response compression via middleware

## Future Enhancements

- [ ] AI-powered intent parsing for natural language queries
- [ ] More sophisticated tax calculators (state-specific)
- [ ] Multi-currency support
- [ ] Advanced retirement planning with inflation scenarios
- [ ] Batch calculation processing
- [ ] Export results to PDF/Excel
- [ ] Collaborative features for financial advisors

## Support

For issues or questions:
1. Check the error message carefully
2. Review the logs for more details
3. Check the `.env` configuration
4. Verify database connectivity
5. Review API documentation at `/api/docs`

## License

MIT License - See LICENSE file for details

## Author

Finance Calculator Team
Version: 1.0.0
