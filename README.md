# Simple bank API

## Project structure
```
bank/
├── .github/
├── alembic/
├── src/
│   ├── api/                    # API layer
│   │   ├── routes/                 # Providing API endpoints
│   │   ├── schemes/                # Validating API requests/responses body
│   │   └── security/               # API security 
│   ├── domain/                 # Domain layer
│   │   ├── entities/               # Representing domain entity in database tables
│   │   ├── repositories/           # Interacting with the infrastructure layer
│   │   └── services/               # Business logic, orchestrate multiple repositories, services
│   ├── infrastructure/         # Infrastructure layer
│   │   ├── database/               # Connecting to database, execute database operations
│   └── settings/
├── tests/
│   ├── integration_tests/      # Integration tests
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