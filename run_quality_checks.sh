#!/bin/bash

# Run flake8 for style checking
echo "Running flake8..."
flake8 app/

# Run black for code formatting
echo "Running black..."
black app/

# Run mypy for type checking
echo "Running mypy..."
mypy app/

# Run bandit for security analysis
echo "Running bandit..."
bandit -r app/ --skip B101

# Run pytest with coverage
echo "Running pytest with coverage..."
pytest --cov=app --cov-report=term-missing --cov-report=html

# Run mutation testing
echo "Running mutation testing..."
mutmut run

# Run performance benchmarks
echo "Running performance benchmarks..."
pytest --benchmark-only

# Run load testing with locust
echo "Running load tests with locust..."
locust -f locustfile.py --headless -u 100 -r 10 -t 1m 