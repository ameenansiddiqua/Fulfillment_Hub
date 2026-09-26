# XYZ Fulfillment Hub

A simple fulfillment management application designed to help XYZ monitor orders, inventory, shipments, and operational issues in one centralized dashboard.

## Features

- Dashboard with fulfillment summary metrics
- Order tracking and filtering
- Order search by Order ID, Customer, or SKU
- Inventory monitoring with low-stock identification
- Inventory search by SKU or product name
- Shipment tracking and status filtering
- Shipment search by Shipment ID, Order ID, or Tracking ID
- Issue tracking with Open and Resolved status
- 12-hour and 24-hour time format
- Dashboard refresh option

## Technologies Used

- Python
- Streamlit
- Pandas
- CSV

## Project Structure

```text
Fulfillment_Hub
├── app.py
├── data
│   ├── orders.csv
│   ├── products.csv
│   ├── inventory.csv
│   ├── shipments.csv
│   └── issues.csv
├── requirements.txt
├── README.md
└── .gitignore
## How to Run

1. Open the project in PyCharm.
2. Open the PyCharm Terminal.
3. Install the required packages:

pip install -r requirements.txt

4. Start the application:

streamlit run app.py

5. Open the Streamlit URL shown in the terminal.

## Data

The application uses dummy CSV data for demonstration purposes. No real store, customer, inventory, or courier system is connected.
