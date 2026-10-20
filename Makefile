BUSID ?=

.PHONY: setup lint lint-fix build upload monitor upload-monitor upload-win attach run-daemon run-daemon-win clean

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

monitor:
	@echo "Opening serial monitor (Press Ctrl+C to exit)..."
	cd firmware && pio device monitor

upload-monitor:
	@echo "Uploading firmware and opening serial monitor..."
	cd firmware && pio run --target upload && pio device monitor

upload-win:
	@echo "Uploading firmware to Arduino R4 via Windows Host..."
	cmd.exe /c start "PIO Upload" powershell.exe -NoLogo -NoExit -Command "cd '$(shell wslpath -m $(PWD)/firmware)'; pio run --target upload"

attach:
	@echo "Attaching Arduino USB device to WSL..."
	powershell.exe -ExecutionPolicy Bypass -File ./scripts/windows/attach_arduino.ps1 $(if $(BUSID),-BusId $(BUSID))

run-daemon:
	@echo "Starting Python daemon..."
	cd daemon && uv run python -m src.main

run-daemon-win:
	@echo "Opening new Windows terminal for the daemon..."
	cmd.exe /c start "R4 Daemon" powershell.exe -NoLogo -NoExit -Command "cd '$$(wslpath -w $$(pwd)/daemon)'; python src/main.py"

clean:
	@echo "Cleaning builds..."
	cd firmware && pio run --target clean
	rm -rf daemon/.venv
