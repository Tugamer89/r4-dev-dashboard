.PHONY: setup lint lint-fix build upload run-daemon clean

setup:
	@echo "Setting up Python environment and pre-commit hooks..."
	cd daemon && uv venv && uv pip install -e .[dev]
	pre-commit install

lint:
	@echo "Running pre-commit on all files..."
	pre-commit run --all-files

lint-fix:
	@echo "Fixing linting issues..."
	cd daemon && uv run ruff check --fix .
	cd daemon && uv run ruff format .
	find firmware/src firmware/include -name "*.cpp" -o -name "*.h" | xargs clang-format -i

build:
	@echo "Building C++ firmware..."
	cd firmware && pio run

upload:
	@echo "Uploading firmware to Arduino R4..."
	cd firmware && pio run --target upload

run-daemon:
	@echo "Starting Python daemon..."
	cd daemon && uv run python -m src.main

clean:
	@echo "Cleaning builds..."
	cd firmware && pio run --target clean
	rm -rf daemon/.venv
