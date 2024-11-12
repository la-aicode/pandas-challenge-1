# Client Data Analysis

This project performs data analysis on a dataset containing client order information. The code calculates financial metrics for each client, confirms specific order totals, and summarizes spending for top clients.

## Project Overview

The analysis includes:
1. **Data Transformation**: Creating columns for subtotal, shipping cost, total price (with tax), line cost, and profit.
2. **Top Client Analysis**: Summing up total units, shipping cost, revenue, and profit for the top 5 clients by quantity ordered.
3. **Order Confirmation**: Confirming the total prices for specific orders to ensure calculations match provided values.

## Files

- `client_dataset.csv`: The CSV file containing the raw client order data.
- `dataAnalysis.py`: The main script that loads, processes, and analyzes the data.
- `README.md`: This file, providing an overview and usage instructions.

## Setup and Usage

1. **Clone the repository** and navigate to the directory:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install the required libraries**:
    The code uses `pandas`. Install it via pip if it’s not already installed:
    ```bash
    pip install pandas
    ```

3. **Run the Script**:
    Execute the script to see the outputs:
    ```bash
    python dataAnalysis.py
    ```

## Code Summary

The following is a summary of the primary functions and calculations:

### 1. Data Transformation

In `dataAnalysis.py`, the following columns are created:
- **Subtotal**: `unit_price * qty`
- **Shipping Price**: `$7 per pound for orders over 50 pounds, $10 per pound otherwise`
- **Total Price**: `subtotal + shipping_price + 9.25% sales tax`
- **Line Cost**: `unit_cost * qty + shipping_price`
- **Profit**: `total_price - line_cost`

### 2. Top Client Analysis

The function `calculate_totals` takes a list of client IDs and computes the total units, shipping, revenue, and profit for each client. The `format_to_millions` function then formats these values in millions for readability.

### 3. Order Confirmation

The code verifies total prices for specific orders. Using the `order_id`, it groups and sums the `total_price` column to ensure the calculated totals match provided values.

Example output for order confirmation:

Order ID 2742071: Expected Total: $152,811.89 Actual Total: $152,811.89 Match: Yes

## Code Snippets

### Confirming Order Totals

This code snippet confirms if specific orders have the correct totals:

```python
# Define Order IDs and Expected Totals
order_ids = [2742071, 2173913, 6128929]
expected_totals = [152811.89, 162388.71, 923441.25]

# Calculate and Print Totals
actual_totals = df[df['order_id'].isin(order_ids)].groupby('order_id')['total_price'].sum()
for order_id, expected_total in zip(order_ids, expected_totals):
    actual_total = actual_totals[order_id]
    print(f"Order ID {order_id}:\n  Expected Total: ${expected_total:,.2f}\n  Actual Total: ${actual_total:,.2f}\n  Match: {'Yes' if actual_total == expected_total else 'No'}\n")
