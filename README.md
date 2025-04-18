# Simple bank API

## Project structure
```
bank/
├── .github/
├── alembic/                # Database migrations
├── src/                    # Source code
│   ├── api/                    # API layer
│   │   ├── routes/                 # Providing API endpoints
│   │   └── schemes/                # Validating API requests/responses body
│   ├── domain/                 # Domain layer
│   │   ├── models/                 # Representing domain entity in database tables
│   │   ├── repositories/           # Interacting with the database via methods corresponding to database operations
│   │   └── services/               # Business logic
│   ├── infrastructure/         # Infrastructure layer
│   │   ├── database/               # Connecting to database, execute database operations
│   └── settings/               # Application settings
├── tests/                  # Testing
│   ├── api_tests/              # Integration tests, calling API routes
│   ├── unit_tests/             # Unit tests
│   └── conftest.py             # Config test
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── main.py                     # Entry point
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Start server
- docker compose up -d [--build]
- docker compose down

## Run tests
- pip install -r requirements.txt
- pytest [--cov-report=html]

## Install pre-commit hook
- pre-commit install