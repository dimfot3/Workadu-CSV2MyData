# Workadu CSV2MyData

This Python utility automates customer management and billing on Workadu, an all-in-one business management platform used for scheduling, ERP, and professional invoicing. By leveraging the Workadu REST API, the tool eliminates manual data entry, transforming raw administrative data into finalized financial records in a single execution.

The workflow processes CSV exports (such as Calendly or Iris data) to identify customers, create new profiles when necessary, and generate detailed line-item invoices. Once published, the tool ensures all invoices are automatically transmitted to the AADE MyData platform, keeping your business fully compliant with Greek tax regulations.


## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Libraries:** `requests`, `PyYAML`
* **Authentication:** Basic Auth (Base64 encoded API Key)

## 📦 Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/yourusername/workadu-invoice-importer.git](https://github.com/yourusername/workadu-invoice-importer.git)
    cd workadu-invoice-importer
    ```

2.  **Install Dependencies:**
    ```bash
    pip install requests pyyaml
    ```

3.  **Prepare Configuration:**
    Create a `config.yaml` file in the root directory:
    ```yaml
    api:
      key: "YOUR_WORKADU_API_KEY"
      base_url: "https://app.workadu.com/api"

    settings:
      series_id: 174862
      vat_percent: 0
      csv_file: "test_invoices.csv"
      sleep_interval: 1.0
    ```

## 📋 CSV Format

The script expects a CSV file with the following header structure:

| Customer Description | Customer Email | Description | Amount |
| :--- | :--- | :--- | :--- |
| Full Name | user@example.com | Service Name | 40.00 |

> **Note:** If the email is missing, the script will generate a randomized placeholder email to ensure the Workadu record is created successfully.

## 🖥️ Usage

Run the importer from your terminal:

```bash
python importer.py
```

---

## ⚖️ License
Distributed under the MIT License. See LICENSE for more information.
