# Contributing to R4 Dev Dashboard

First off, thank you for taking the time to contribute! 🎉 We appreciate your help in making the R4 Dev Dashboard better.

Please take a moment to review this document to make the contribution process easy and effective for everyone involved.

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to the project maintainers.

---

## How Can I Contribute?

### 1. Reporting Bugs
* **Check existing issues** first to avoid duplicates.
* **Use the issue template** and provide a clear description of the problem, steps to reproduce, and your environment (e.g., Arduino board version, OS, Python version).

### 2. Suggesting Enhancements
* Open an issue to discuss your proposal before jumping into heavy development.
* Clearly explain why the feature would be useful and how it fits into the project architecture.

### 3. Pull Requests (PRs)
1. Fork the repository and create your branch from `main` (or the appropriate working branch).
2. Ensure your code follows the project's formatting and linting rules.
3. Run local checks/tests before submitting.
4. Open a Pull Request with a clear description of changes.

---

## Project Structure Overview

This repository consists of two main subsystems:
* **`firmware/`**: C++ code targeting the Arduino/R4 platform using **PlatformIO**.
* **`daemon/`**: Python application running via **uv** for system monitoring and WebSocket communication.

---

## Development Setup & Guidelines

### Firmware (`firmware/`)
* **Toolchain:** [PlatformIO](https://platformio.org/)
* **Formatting:** C++ files are formatted using `clang-format`. Check out the `.clang-format` configuration in the root directory.
* **Building:** You can use PlatformIO CLI or your preferred IDE integration to compile and flash the firmware:
  ```bash
  cd firmware
  pio run
  ```

### Daemon (`daemon/`)
* **Toolchain:** Python managed by [uv](https://github.com/astral-sh/uv).
* **Dependencies:** Defined inside `daemon/pyproject.toml` and locked via `daemon/uv.lock`.
* **Running/Testing:** Use `uv` to manage environment and execution inside the `daemon/` folder.

---

## Linter & Code Quality Checks

We use automated linters and pre-commit hooks to keep our code clean:
* **Pre-commit Hooks:** Install and run pre-commit locally before committing:
  ```bash
  pip install pre-commit
  pre-commit install
  pre-commit run --all-files
  ```
* **Linters:** GitHub Actions workflows validate C++ (`cpp-linter`) and Python (`python-linter`) syntax on every push and pull request. Make sure your local edits pass these checks.

---

## Commit Message Guidelines

We follow the **Conventional Commits** specification. This ensures clean commit histories and allows tools like `release-please` to automate versioning and changelogs.

Format:
```text
<type>(<scope>): <short description>
```

Common types:
* `feat`: A new feature
* `fix`: A bug fix
* `docs`: Documentation only changes
* `style`: Changes that do not affect the meaning of the code (formatting, missing semi-colons, etc.)
* `refactor`: A code change that neither fixes a bug nor adds a feature
* `chore`: Changes to the build process or auxiliary tools (like dependency updates)

Example:
```text
docs: add CONTRIBUTING.md guide
```
