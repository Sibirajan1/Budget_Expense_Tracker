import pandas as pd
import os

# Folder containing the extracted CSVs
folder_path = r"S:/PYTHON/extracted_items"

# List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

# Merge all CSV files into one DataFrame
dataframes = []
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except Exception:
        df = pd.read_csv(file_path, encoding='latin1')
    dataframes.append(df)

merged_df = pd.concat(dataframes, ignore_index=True)

# ✅ Step 1: Drop Duplicate Rows
merged_df.drop_duplicates(inplace=True)

# ✅ Step 2: Handle Price Columns
possible_price_cols = ['price', 'Price', 'Discounted Price (Rs.)', 'discounted_price_(rs.)', 'Unit_Price']
for col in possible_price_cols:
    if col in merged_df.columns:
        merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')
        merged_df[col].fillna(merged_df[col].median(), inplace=True)

# ✅ Step 3: Handle Text Columns (e.g., product/category names)
text_cols = ['product_name', 'Product Name', 'commodity', 'category', 'Category']
for col in text_cols:
    if col in merged_df.columns:
        merged_df[col] = merged_df[col].astype(str).str.strip().str.lower()

# ✅ Step 4: Drop rows where key fields like product name or price are still missing
key_columns = ['product_name', 'Product Name', 'commodity', 'price', 'Discounted Price (Rs.)']
cols_to_check = [col for col in key_columns if col in merged_df.columns]
merged_df.dropna(subset=cols_to_check, how='all', inplace=True)

# ✅ Step 5: Save the cleaned dataset
cleaned_path = os.path.join(folder_path, "cleaned_merged_data.csv")
merged_df.to_csv(cleaned_path, index=False)
print(f"\n✅ Cleaned data saved to: {cleaned_path}")
