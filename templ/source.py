
import pandas as pd
# Path to cleaned CSV file
cleaned_csv_path = "S:/PYTHON/extracted_items/modified_stacked_dataset.csv"

# Load the cleaned data
merged_df = pd.read_csv(cleaned_csv_path)

# Convert prices to numeric if applicable
if 'Discounted Price (Rs.)' in merged_df.columns:
    merged_df['Discounted Price (Rs.)'] = pd.to_numeric(merged_df['Discounted Price (Rs.)'], errors='coerce')

# User input items and quantities
shopping_list = []
while True:
    item_name = input("Enter item name (or 'done' to finish): ")
    if item_name.lower() == 'done':
        break

    quantity = int(input(f"Enter quantity for {item_name}: "))

    # Search for item price
    if 'Product Name' in merged_df.columns:
        item_data = merged_df[merged_df['Product Name'].str.contains(item_name, case=False, na=False)]
    elif 'product_name' in merged_df.columns:
        item_data = merged_df[merged_df['product_name'].str.contains(item_name, case=False, na=False)]
    else:
        print("No recognizable product name column found.")
        continue

    if not item_data.empty:
        min_price = item_data['Discounted Price (Rs.)'].min()
        max_price = item_data['Discounted Price (Rs.)'].max()
        avg_price = item_data['Discounted Price (Rs.)'].mean()

        total_price = avg_price * quantity
        shopping_list.append([item_name, quantity, min_price, max_price, total_price])
    else:
        print(f"Item '{item_name}' not found in dataset.")

# Convert to DataFrame and display
shopping_df = pd.DataFrame(shopping_list, columns=['Item', 'Quantity', 'Min Price', 'Max Price', 'Total Predicted Price'])

# Calculate total predicted bill
total_predicted_bill = shopping_df['Total Predicted Price'].sum()

print("\nFinal Shopping List:")
print(shopping_df.to_string(index=False))
print(f"\nTotal Predicted Bill: Rs. {total_predicted_bill:.2f}")
