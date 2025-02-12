.PHONY: help install-uv setup clean install dev-install update lock lint format lint-check

# Default shell
SHELL := /bin/bash

# Python version
PYTHON_VERSION ?= 3.12.3

# Source code directories to lint/format
PYTHON_SOURCES = .

help:
	@echo "Available commands:"
	@echo "  make install-uv    : Install uv package manager"
	@echo "  make setup         : Initial project setup with uv"
	@echo "  make lock          : Generate/update uv.lock"
	@echo "  make install       : Install production dependencies from lock file"
	@echo "  make dev-install   : Install development dependencies from lock file"
	@echo "  make update        : Update dependencies and regenerate lock file"
	@echo "  make clean         : Remove build/temporary files"
	@echo "  make format        : Format code using black"
	@echo "  make lint          : Run all linters and formatters"
	@echo "  make lint-check    : Check linting without making changes"

install-uv:
	@echo "Installing uv package manager..."
	@if command -v curl >/dev/null 2>&1; then \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	else \
		echo "Error: curl is required to install uv. Please install curl first."; \
		exit 1; \
	fi

setup: install-uv
	@echo "Setting up Python virtual environment with uv..."
	@uv venv

lock:
	@echo "Generating lock file from pyproject.toml..."
	@uv pip compile pyproject.toml --output-file uv.lock
	@echo "Lock file generated successfully!"

install: setup
	@echo "Installing dependencies from lock file..."
	@if [ -f "uv.lock" ]; then \
		uv pip install -r uv.lock; \
	else \
		echo "Error: uv.lock not found. Run 'make lock' first."; \
		exit 1; \
	fi

dev-install: setup
	@echo "Installing development dependencies..."
	@if [ -f "uv.lock" ]; then \
		uv pip install -r uv.lock; \
		uv pip install --dev-requirements .; \
	else \
		echo "Error: uv.lock not found. Run 'make lock' first."; \
		exit 1; \
	fi

update:
	@echo "Updating dependencies and regenerating lock file..."
	@uv pip compile pyproject.toml --output-file uv.lock --upgrade
	@make install

format:
	@echo "Formatting code with black..."
	@black $(PYTHON_SOURCES)

lint-check:
	@echo "Checking code formatting with black..."
	@black --check $(PYTHON_SOURCES)
	@echo "Running ruff checks..."
	@ruff check $(PYTHON_SOURCES)

lint: format
	@echo "Running ruff checks..."
	@ruff check $(PYTHON_SOURCES)
	@ruff format $(PYTHON_SOURCES)
	@echo "Linting complete!"

clean:
	@echo "Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .pytest_cache/
	@rm -rf .coverage
	@rm -rf .mypy_cache/
	@rm -rf __pycache__/
	@rm -rf ./**/__pycache__/
	@rm -rf uv.lock
	@echo "Clean complete!"