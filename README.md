Workadu Invoice Importer
A lightweight Python utility to automate customer creation and invoice generation on the Workadu platform via CSV data.

Features
Automated Workflow: Creates customers, generates draft invoices, adds line items, and publishes them in one sequence.

CSV Integration: Processes bulk data from standard exports (e.g., Iris/Calendly).

Configurable: Manage API credentials and tax settings via external YAML configuration.

Safety First: Includes rate-limiting (sleep intervals) and logging for process tracking.

Tech Stack
Language: Python 3.10+

Libraries: requests, PyYAML

API: Workadu REST API (Basic Auth)

Setup
Clone the repository:

Bash

git clone https://github.com/yourusername/workadu-invoice-importer.git
cd workadu-invoice-importer
Install dependencies:

Bash

pip install -r requirements.txt
Configure the application: Create a config.yaml file in the root directory (refer to config.example.yaml):

YAML

api:
  key: "your_workadu_api_key"
  base_url: "https://app.workadu.com/api"
settings:
  series_id: 174862
  vat_percent: 0
  csv_file: "data.csv"
  sleep_interval: 1.0
Usage
Ensure your CSV file matches the expected headers (Customer Description, Customer Email, Description, Amount), then run:

Bash

python importer.py
Security Note
Never commit your config.yaml file containing your API key. This repository includes a .gitignore to prevent sensitive data leaks.

Suggested .gitignore
To keep the repo professional, ensure these files are ignored:

Plaintext

# Configuration
config.yaml

# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Data
*.csv
