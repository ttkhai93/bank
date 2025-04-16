# Simple bank API

## Start server
- docker compose up -d [--build]
- docker compose down

## Run tests
- pip install -r requirements.txt
- pytest [--cov] [--cov-fail-under=90] [--cov-report=html]

## Install pre-commit hook
- pre-commit install