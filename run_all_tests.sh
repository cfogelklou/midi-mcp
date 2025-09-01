#!/bin/bash

# Script to run all pytest tests
# Usage: ./run_all_tests.sh

set -e  # Exit on any error

echo "🧪 Running all pytest tests..."
echo "================================"

# Run pytest with verbose output and coverage if available
if command -v pytest &> /dev/null; then
    # Check if pytest-cov is available for coverage reporting
    if python -c "import pytest_cov" 2>/dev/null; then
        echo "Running tests with coverage..."
        pytest tests/ -v --cov=src/midi_mcp --cov-report=term-missing
    else
        echo "Running tests without coverage (install pytest-cov for coverage reports)..."
        pytest tests/ -v
    fi
else
    echo "❌ pytest not found. Please install with: pip install pytest"
    exit 1
fi

echo ""
echo "✅ Test run complete!"