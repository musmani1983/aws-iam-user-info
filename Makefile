# Makefile for running Python script, tests, and installing dependencies

# Name of the Python script
SCRIPT = retrieve_iam_info.py

# Name of the test script
TEST_SCRIPT = test_retrieve_iam_info.py

# Name of the virtual environment directory
VENV_DIR = venv

# Helper function to set up the virtual environment and install dependencies
define setup_venv
    python3 -m venv $(VENV_DIR)
    @echo "Activating virtual environment..."
    @. $(VENV_DIR)/bin/activate && pip install -r requirements.txt
endef

# Target to create the virtual environment, activate, and install dependencies
setup:
    $(call setup_venv)

# Target to run the tests using unittest within the virtual environment
test: setup
    $(VENV_DIR)/bin/python -m unittest $(TEST_SCRIPT)

# Target to run the Python script with the specified output format (CSV or JSON)
run-csv: setup
    $(VENV_DIR)/bin/python $(SCRIPT) --format csv

run-json: setup
    $(VENV_DIR)/bin/python $(SCRIPT) --format json

# Target to display a list of available targets and their descriptions
help:
    @echo "Available targets:"
    @echo "  setup    - Create virtual environment and install dependencies"
    @echo "  test     - Run tests using unittest"
    @echo "  run-csv  - Run the Python script and save as CSV (default)"
    @echo "  run-json - Run the Python script and save as JSON"
    @echo "  help     - Display this help message (you are here)"
    @echo ""
    @echo "Usage for 'run-csv' and 'run-json' targets:"
    @echo "  make run-csv"
    @echo "  make run-json"
    @echo "For more information on each target, use 'make <target> help'."
    @echo ""

# Default target (make) runs the script in CSV format
default: run-csv
