.PHONY: lint format check test clean install dev-install

# Python and pip commands
PYTHON := python3
PIP := pip

# Source directories
SRC_DIR := src
TEST_DIR := tests

# Linting and formatting commands
lint: lint-black lint-isort lint-flake8 lint-mypy lint-vulture

lint-black:
	@echo "Running Black (code formatter check)..."
	black --check --diff $(SRC_DIR)

lint-isort:
	@echo "Running isort (import sorter check)..."
	isort --check-only --diff $(SRC_DIR)

lint-flake8:
	@echo "Running flake8 (style guide enforcement)..."
	flake8 $(SRC_DIR)

lint-mypy:
	@echo "Running mypy (type checking)..."
	mypy $(SRC_DIR)

lint-vulture:
	@echo "Running vulture (dead code detection)..."
	vulture $(SRC_DIR) --min-confidence 60

format: format-black format-isort

format-black:
	@echo "Running Black (code formatter)..."
	black $(SRC_DIR)

format-isort:
	@echo "Running isort (import sorter)..."
	isort $(SRC_DIR)

check: lint test
	@echo "All checks passed!"

test:
	@echo "Running tests..."
	pytest

clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .mypy_cache/ .pytest_cache/

install:
	@echo "Installing package..."
	$(PIP) install -e .

dev-install:
	@echo "Installing package with development dependencies..."
	$(PIP) install -e ".[dev]"

help:
	@echo "Available commands:"
	@echo "  lint          - Run all linting tools"
	@echo "  lint-black    - Run Black formatter check"
	@echo "  lint-isort    - Run isort import checker"
	@echo "  lint-flake8   - Run flake8 style checker"
	@echo "  lint-mypy     - Run mypy type checker"
	@echo "  lint-vulture  - Run vulture dead code detector"
	@echo "  format        - Format code with Black and isort"
	@echo "  format-black  - Format code with Black"
	@echo "  format-isort  - Sort imports with isort"
	@echo "  check         - Run lint and test"
	@echo "  test          - Run tests"
	@echo "  clean         - Clean up build artifacts"
	@echo "  install       - Install package"
	@echo "  dev-install   - Install with dev dependencies"
	@echo "  help          - Show this help message"