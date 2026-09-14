#!/usr/bin/env bash
# CAD CI/CD Sandbox Simulation Runner (Linux / macOS)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "==================================================="
echo "  Starting CAD CI/CD Local Sandbox Simulation...   "
echo "==================================================="

python3 "$SCRIPT_DIR/ci_sandbox.py" --all

echo ""
echo "Running Pytest Verification Suite..."
python3 -m pytest "$PROJECT_ROOT/tests" -v

echo "All CI checks passed successfully!"
