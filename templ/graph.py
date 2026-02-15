
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

# Path to cleaned CSV file
cleaned_csv_path = "S:/PYTHON/extracted_items/cleaned_dataset_for_model.csv"

# Load the cleaned data
merged_df = pd.read_csv(cleaned_csv_path, low_memory=False)

# Rename product column if needed
if 'Product_Name_Combined' in merged_df.columns:
    merged_df = merged_df.rename(columns={"Product_Name_Combined": "Product Name"})

# Convert price columns to numeric
merged_df['Discounted Price (Rs.)'] = pd.to_numeric(merged_df.get('Discounted Price (Rs.)'), errors='coerce')
merged_df['Original Price (Rs.)'] = pd.to_numeric(merged_df.get('Original Price (Rs.)'), errors='coerce')

# Get user budget with validation
while True:
    try:
        budget = int(input("Enter your Budget Amount: "))
        break
    except ValueError:
        print("⚠️ Please enter a valid numeric amount for the budget.")

# User input items and quantities
shopping_list = []
actual_prices = []
predicted_prices = []

while True:
    item_name = input("Enter item name (or 'done' to finish): ")
    if item_name.lower() == 'done':
        break

    # Get quantity with validation
    while True:
        try:
            quantity = int(input(f"Enter quantity for {item_name}: "))
            if quantity <= 0:
                print("⚠️ Quantity must be a positive integer.")
                continue
            break
        except ValueError:
            print("⚠️ Please enter a valid number for quantity.")

    # Find item data
    if 'Product Name' in merged_df.columns:
        item_data = merged_df[merged_df['Product Name'].str.contains(item_name, case=False, na=False)]
    else:
        print("❌ No recognizable product name column found.")
        continue

    if not item_data.empty:
        # Calculate predicted price
        avg_price = item_data['Discounted Price (Rs.)'].mean()
        min_price = item_data['Discounted Price (Rs.)'].min()
        max_price = item_data['Discounted Price (Rs.)'].max()
        total_price = avg_price * quantity if not np.isnan(avg_price) else 0

        # Estimate actual price
        actual_avg = item_data['Original Price (Rs.)'].mean()
        total_actual = actual_avg * quantity if not np.isnan(actual_avg) else None

        # Store prices for evaluation
        if total_actual is not None:
            actual_prices.append(total_actual)
            predicted_prices.append(total_price)

        # Add to shopping list
        shopping_list.append([item_name, quantity, min_price, max_price, total_price])
    else:
        print(f"❌ Item '{item_name}' not found in dataset.")

# Create output DataFrame
shopping_df = pd.DataFrame(shopping_list, columns=['Item', 'Quantity', 'Min Price', 'Max Price', 'Total Predicted Price'])
total_predicted_bill = shopping_df['Total Predicted Price'].sum()

# Print final shopping list
print("\n🛒 Final Shopping List:")
print(shopping_df.to_string(index=False))
print(f"\n💰 Total Predicted Bill: Rs. {total_predicted_bill:.2f}")

def plot_price_range_bar(shopping_df):
    plt.figure(figsize=(10, 5))
    x = shopping_df['Item']
    min_prices = shopping_df['Min Price']
    max_prices = shopping_df['Max Price']
    
    plt.bar(x, min_prices, label='Min Price', alpha=0.7)
    plt.bar(x, max_prices, label='Max Price', alpha=0.7, bottom=min_prices)
    plt.xlabel("Items")
    plt.ylabel("Price")
    plt.title("Price Range per Item")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Budget comparison
if total_predicted_bill < budget:
    print(f"\n✅ Good news! Your estimated bill of Rs. {total_predicted_bill:.2f} is within your budget of Rs. {budget:.2f}.")
    print("You can comfortably buy everything on your list and still have some money left!")
elif total_predicted_bill == budget:
    print(f"\n⚖️ Perfect match! Your estimated bill is exactly Rs. {total_predicted_bill:.2f}, which is equal to your budget.")
    print("You can purchase everything on your list, but there's no margin for extras.")
else:
    print(f"\n⚠️ Budget Alert! Your estimated bill of Rs. {total_predicted_bill:.2f} exceeds your budget of Rs. {budget:.2f}.")
    print("You may need to reduce some items or quantities to stay within budget.")

plot_price_range_bar(shopping_df)


# Evaluate model predictions
if actual_prices and predicted_prices:
    mae = mean_absolute_error(actual_prices, predicted_prices)
    mse = mean_squared_error(actual_prices, predicted_prices)
    rmse = mse ** 0.5
    r2 = r2_score(actual_prices, predicted_prices)
    approx_accuracy = max(0.0, min(r2 * 100, 100))

    print("\n📊 Model Evaluation Metrics:")
    print(f"R² Score: {r2:.4f}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"Estimated Accuracy (approx): {approx_accuracy:.2f}%")
else:
    print("\n⚠️ Not enough actual price data to compute model evaluation metrics.")

    
# Budget comparison chart
plt.figure(figsize=(6,4))
labels = ['Budget', 'Predicted Expense']
values = [budget, total_predicted_bill]
colors = ['green' if budget >= total_predicted_bill else 'red', 'blue']

plt.bar(labels, values, color=colors)
plt.title("Budget vs Predicted Expense")
plt.ylabel("Amount (Rs.)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()


