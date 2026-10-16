# Guess Game App

A simple number-guessing game built with Python and FastAPI, with a browser-based user interface.

This project is a practical learning application for developing and testing application logic, REST APIs, and browser UI behaviour.

## Project Structure

```text
guess-game-app/
├── src/                 # Python application and backend
├── ui/                  # HTML, CSS, and JavaScript frontend
├── tests/               # Unit tests
├── .gitignore
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Technology Stack

- **Python** — application logic
- **FastAPI** — backend API
- **pytest** — unit testing
- **HTML, CSS, JavaScript** — frontend

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git

### Setup

1. Clone the repository.

   ```bash
   git clone <repository-url>
   cd guess-game-app
   ```

2. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   ```

   Linux/macOS:

   ```bash
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install the dependencies.

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Run instructions will be added once the application entry point and API routes are implemented.

## Running Tests

Run the unit tests with:

```bash
pytest
```

## Automation Testing

The application will be tested using separate repositories for:

- pytest + Selenium
- pytest + Playwright
- Robot Framework

These repositories will contain browser automation tests for the application's user-facing behaviour.

## Development Approach

The application will evolve through small, meaningful requirements. Each feature will be implemented, tested, reviewed, and committed to Git.

The focus is on understandable code, meaningful test scenarios, and practical implementation.
