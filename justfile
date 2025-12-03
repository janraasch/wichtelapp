# Default task
default:
    @just --list

# Run development server
dev:
    python manage.py runserver

# Run tests
test:
    python manage.py test

# Check linting (no fixes)
lint:
    ruff check .
    djhtml --check wichtel/templates/

# Auto-fix and format
fmt:
    ruff check --fix .
    ruff format .
    djhtml wichtel/templates/

# CI: lint + test
ci: lint test
