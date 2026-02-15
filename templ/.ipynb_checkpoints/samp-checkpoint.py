import pandas as pd
import zipfile
import os

# Path to merged ZIP file
merged_zip_path = "S:/PYTHON/merged_items.zip"  # Use the actual location
extract_path = "S:/PYTHON/extracted_items"  # Folder where files will be extracted

# Ensure the extraction directory exists
os.makedirs(extract_path, exist_ok=True)

# Extract ZIP file
with zipfile.ZipFile(merged_zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Load all CSV files and merge them
dataframes = []
for file in os.listdir(extract_path):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(extract_path, file))
        dataframes.append(df)

# Concatenate all dataframes into one merged dataset
merged_df = pd.concat(dataframes, ignore_index=True)

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
    item_data = merged_df[merged_df['Product Name'].str.contains(item_name, case=False, na=False)]
    if not item_data.empty:
        min_price = item_data['Discounted Price (Rs.)'].min()
        max_price = item_data['Discounted Price (Rs.)'].max()
        avg_price =  item_data['Discounted Price (Rs.)'].mean() # Adjusted calculation for avg_price
        
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
