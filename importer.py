# Workadu Invoice Importer
# Copyright (c) 2026 Fotiou Dimitrios
# Licensed under the MIT License

import base64
import requests
import csv
import time
import yaml
import logging
import random
import string
from typing import Optional, Dict, Any

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WorkaduClient:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.api_key = self.config['api']['key']
        self.base_url = self.config['api']['base_url']
        self.headers = self._get_headers()

    def _load_config(self, path: str) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _get_headers(self) -> dict:
        token = base64.b64encode(f"{self.api_key}:".encode()).decode()
        return {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json"
        }

    def get_next_invoice_number(self, series_id: int) -> int:
        url = f"{self.base_url}/series/{series_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        # Adjusted based on your original logic
        data = response.json().get("data", [])
        return data[0]['last_number'] + 1 if data else 1

    def create_customer(self, fullname: str, email: str) -> str:
        url = f"{self.base_url}/customers/"
        payload = {"fullname": fullname, "email": email}
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()['data']['id']

    def create_invoice(self, customer_id: str, series_id: int, invoice_num: int, vat_per: int, payment_type) -> Optional[Dict]:
        url = f"{self.base_url}/invoices/"
        payload = {
            "customer_id": customer_id,
            "series_id": series_id,
            "invoice_num": invoice_num,
            "discount_percent": 0,
            "vat_percent": vat_per,
            "currency": "EUR",
            "payment_type": payment_type,
            "includes_vat": True
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("data")
        logging.error(f"Invoice creation failed: {response.text}")
        return None

    def create_invoice_line(self, invoice_id: str, description: str, amount: float) -> bool:
        url = f"{self.base_url}/invoiceline/"
        payload = {
            "invoice_id": invoice_id,
            "description": description,
            "amount": amount,
            "quantity": 1
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.status_code == 200

    def publish_invoice(self, invoice_id: str, send_email: bool = False) -> bool:
        url = f"{self.base_url}/invoices/publish/"
        payload = {"invoice_id": invoice_id, "send_email": send_email}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.status_code == 200

def generate_random_email() -> str:
    random_str = "".join(random.choices(string.ascii_lowercase, k=6))
    return f"{random_str}@gmail.com"

def main():
    client = WorkaduClient()
    settings = client.config['settings']
    
    try:
        with open(settings['csv_file'], newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                name = row.get("Customer Description", "Unknown Customer")
                email = row.get("Customer Email") or generate_random_email()
                
                # Parsing logic
                raw_desc = row.get("Description", "")
                
                try:
                    line_amount = float(row.get("Amount", 0))
                except ValueError:
                    logging.warning(f"Skipping {name}: Invalid amount format.")
                    continue

                # Workflow Execution
                logging.info(f"Processing invoice for: {name}")
                
                inv_num = client.get_next_invoice_number(settings['series_id'])
                cust_id = client.create_customer(name, email)
                
                invoice = client.create_invoice(
                    cust_id, 
                    settings['series_id'], 
                    inv_num, 
                    settings['vat_percent'],
                    settings['payment_type']
                )

                if invoice and (inv_id := invoice.get("id")):
                    client.create_invoice_line(inv_id, raw_desc, line_amount)
                    client.publish_invoice(inv_id)
                    logging.info(f"Successfully completed workflow for {name}")
                
                time.sleep(settings['sleep_interval'])

    except FileNotFoundError:
        logging.error(f"CSV file not found: {settings['csv_file']}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

