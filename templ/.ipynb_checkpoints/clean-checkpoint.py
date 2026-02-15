import pandas as pd
import zipfile
import os

# Path to merged ZIP file & extraction location
merged_zip_path = "S:/PYTHON/merged_items.zip"  # Update with your correct path
extract_path = "S:/PYTHON/extracted_items"

# Extract ZIP file
with zipfile.ZipFile(merged_zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# Load all CSV files into a list
dataframes = []
for file in os.listdir(extract_path):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(extract_path, file))
        dataframes.append(df)

# Merge all CSVs into one DataFrame
merged_df = pd.concat(dataframes, ignore_index=True)

# ✅ Step 1: Print Available Columns
print("✅ Available Columns in Dataset:", list(merged_df.columns))

# ✅ Step 2: Standardize Column Names (Lowercase & Remove Spaces)
merged_df.columns = merged_df.columns.str.lower().str.replace(" ", "_")

# ✅ Step 3: Handle Missing Values
merged_df.dropna(how='all', inplace=True)  # Remove empty rows
if "discounted_price_(rs.)" in merged_df.columns:
    merged_df["discounted_price_(rs.)"].fillna(merged_df["discounted_price_(rs.)"].median(), inplace=True)

# ✅ Step 4: Convert Data Types
if "discounted_price_(rs.)" in merged_df.columns:
    merged_df["discounted_price_(rs.)"] = pd.to_numeric(merged_df["discounted_price_(rs.)"], errors="coerce")

if "date" in merged_df.columns:
    merged_df["date"] = pd.to_datetime(merged_df["date"], errors="coerce")

# ✅ Step 5: Remove Duplicates
merged_df.drop_duplicates(inplace=True)

# ✅ Step 6: Clean Text Data (Product Names)
# Check if the column exists before cleaning
if "product_name" in merged_df.columns:
    merged_df["Product_Name"] = merged_df["Product_Name"].astype(str).str.strip().str.lower()
elif "product name" in merged_df.columns:
    merged_df["Product Name"] = merged_df["Product Name"].astype(str).str.strip().str.lower()
else:
    print("⚠️ Warning: 'product_name' or 'product name' column not found in dataset!")

# ✅ Step 7: Save the cleaned dataset
cleaned_file_path = "S:/PYTHON/cleaned_items.csv"
merged_df.to_csv(cleaned_file_path, index=False)

print(f"\n✅ Data cleaning completed! Cleaned file saved at: {cleaned_file_path}")
