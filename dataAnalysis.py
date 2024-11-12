import pandas as pd

# Load the CSV data into `df`
df = pd.read_csv('client_dataset.csv')

# Verify that the necessary columns are present; create them if not.
if 'subtotal' not in df.columns:
    df['subtotal'] = df['unit_price'] * df['qty']

if 'shipping_price' not in df.columns:
    df['shipping_price'] = df.apply(lambda x: 7 * x['unit_weight'] * x['qty'] if x['unit_weight'] > 50 else 10 * x['unit_weight'] * x['qty'], axis=1)

if 'total_price' not in df.columns:
    df['total_price'] = (df['subtotal'] + df['shipping_price']) * 1.0925  # Adding sales tax

if 'line_cost' not in df.columns:
    df['line_cost'] = (df['unit_cost'] * df['qty']) + df['shipping_price']

if 'profit' not in df.columns:
    df['profit'] = df['total_price'] - df['line_cost']

# Functions for analysis
def calculate_totals(dataframe, client_ids):
    """
    Calculate total units, shipping, revenue, and profit for given client IDs.
    """
    client_data = dataframe[dataframe['client_id'].isin(client_ids)]
    summary = client_data.groupby('client_id').agg({
        'qty': 'sum',
        'shipping_price': 'sum',
        'total_price': 'sum',
        'profit': 'sum'
    }).reset_index()
    return summary

def format_to_millions(value):
    """
    Convert values to millions for easy readability.
    """
    return round(value / 1_000_000, 2)

# Calculate summary for top 5 clients and format columns to millions
client_summary = calculate_totals(df, [33615, 66037, 46820, 38378, 24741])
client_summary[['qty', 'shipping_price', 'total_price', 'profit']] = client_summary[
    ['qty', 'shipping_price', 'total_price', 'profit']
].applymap(format_to_millions)

# Rename columns for presentation
client_summary.columns = ['Client ID', 'Total Units (M)', 'Total Shipping (M)', 'Total Revenue (M)', 'Total Profit (M)']
client_summary = client_summary.sort_values(by='Total Profit (M)', ascending=False)

# Display summary
print(client_summary)


#Get the order ID to confirm the work and print it.

# Define the Order IDs and expected total prices
order_ids = [2742071, 2173913, 6128929]
expected_totals = [152811.89, 162388.71, 923441.25]

# Calculate the actual total prices for each specified Order ID
actual_totals = df[df['order_id'].isin(order_ids)].groupby('order_id')['total_price'].sum()

# Display the results with both actual and expected values for comparison
for order_id, expected_total in zip(order_ids, expected_totals):
    actual_total = actual_totals[order_id]
    print(f"Order ID {order_id}:")
    print(f"  Expected Total: ${expected_total:,.2f}")
    print(f"  Actual Total:   ${actual_total:,.2f}")
    print(f"  Match: {'Yes' if actual_total == expected_total else 'No'}\n")
