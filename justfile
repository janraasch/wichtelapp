# Default task
default:
    @just --list

# Run development server
dev:
    uv run python manage.py runserver

# Run tests
test:
    uv run python manage.py test

# Check linting (no fixes)
lint:
    uv run ruff check .
    uv run djhtml --check wichtel/templates/

# Auto-fix and format
fmt:
    uv run ruff check --fix .
    uv run ruff format .
    uv run djhtml wichtel/templates/

# CI: lint + test
ci: lint test
