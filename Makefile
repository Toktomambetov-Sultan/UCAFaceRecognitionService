.PHONY: setup venv install migrate run test docker-build docker-up docker-down clean help

# Variables
PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/pip
MANAGE = $(VENV)/bin/python manage.py

help:
	@echo "Available commands:"
	@echo "  make setup        - Create virtual environment and install dependencies"
	@echo "  make venv         - Create virtual environment only"
	@echo "  make install      - Install dependencies"
	@echo "  make migrate      - Run database migrations"
	@echo "  make run          - Start development server"
	@echo "  make test         - Run tests"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make clean        - Remove virtual environment and cache files"

setup: venv install

venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created. Activate it with:"
	@echo "source $(VENV)/bin/activate  # On Linux/Mac"
	@echo ".\$(VENV)\Scripts\activate  # On Windows"

install:
	@echo "Installing dependencies..."
	$(PIP) install -r requirements.txt

migrate:
	@echo "Running migrations..."
	$(MANAGE) makemigrations
	$(MANAGE) migrate

run:
	@echo "Starting development server..."
	$(MANAGE) runserver

test:
	@echo "Running tests..."
	$(MANAGE) test

docker-build:
	@echo "Building Docker image..."
	docker-compose -f test.yml build

docker-up:
	@echo "Starting Docker containers..."
	docker-compose -f test.yml up

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose -f test.yml down

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} + 