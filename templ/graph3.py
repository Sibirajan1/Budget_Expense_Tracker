import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

# Load the cleaned dataset
cleaned_csv_path = "S:/PYTHON/extracted_items/cleaned_dataset_for_model.csv"
merged_df = pd.read_csv(cleaned_csv_path, low_memory=False)

# ✅ Convert Unified_Date to datetime
merged_df['Unified_Date'] = pd.to_datetime(merged_df['Unified_Date'], errors='coerce')

# Rename column if needed
if 'Product_Name_Combined' in merged_df.columns:
    merged_df = merged_df.rename(columns={"Product_Name_Combined": "Product Name"})

# Convert price columns to numeric
merged_df['Discounted Price (Rs.)'] = pd.to_numeric(merged_df.get('Discounted Price (Rs.)'), errors='coerce')
merged_df['Original Price (Rs.)'] = pd.to_numeric(merged_df.get('Original Price (Rs.)'), errors='coerce')

# Get user budget
while True:
    try:
        budget = int(input("Enter your Budget Amount: "))
        break
    except ValueError:
        print("⚠️ Please enter a valid numeric amount for the budget.")

# User input
shopping_list = []
actual_prices = []
predicted_prices = []

while True:
    item_name = input("Enter item name (or 'done' to finish): ")
    if item_name.lower() == 'done':
        break

    while True:
        try:
            quantity = int(input(f"Enter quantity for {item_name}: "))
            if quantity <= 0:
                print("⚠️ Quantity must be positive.")
                continue
            break
        except ValueError:
            print("⚠️ Invalid number for quantity.")

    item_data = merged_df[merged_df['Product Name'].str.contains(item_name, case=False, na=False)]

    if not item_data.empty:
        avg_price = item_data['Discounted Price (Rs.)'].mean()
        min_price = item_data['Discounted Price (Rs.)'].min()
        max_price = item_data['Discounted Price (Rs.)'].max()
        total_price = avg_price * quantity if not np.isnan(avg_price) else 0

        actual_avg = item_data['Original Price (Rs.)'].mean()
        total_actual = actual_avg * quantity if not np.isnan(actual_avg) else None

        if total_actual is not None:
            actual_prices.append(total_actual)
            predicted_prices.append(total_price)

        shopping_list.append([item_name, quantity, min_price, max_price, total_price])
    else:
        print(f"❌ Item '{item_name}' not found in dataset.")

# Shopping DataFrame
shopping_df = pd.DataFrame(shopping_list, columns=['Item', 'Quantity', 'Min Price', 'Max Price', 'Total Predicted Price'])
total_predicted_bill = shopping_df['Total Predicted Price'].sum()

# Show shopping list
print("\n🛒 Final Shopping List:")
print(shopping_df.to_string(index=False))
print(f"\n💰 Total Predicted Bill: Rs. {total_predicted_bill:.2f}")

# Budget comparison
if total_predicted_bill < budget:
    print(f"\n✅ You're within your budget of Rs. {budget:.2f}.")
elif total_predicted_bill == budget:
    print(f"\n⚖️ Your bill exactly matches the budget: Rs. {budget:.2f}.")
else:
    print(f"\n⚠️ Your bill of Rs. {total_predicted_bill:.2f} exceeds your budget of Rs. {budget:.2f}.")

# Evaluation metrics
if actual_prices and predicted_prices:
    mae = mean_absolute_error(actual_prices, predicted_prices)
    mse = mean_squared_error(actual_prices, predicted_prices)
    rmse = mse ** 0.5
    r2 = r2_score(actual_prices, predicted_prices)
    accuracy = max(0.0, min(r2 * 100, 100))

    print("\n📊 Model Evaluation Metrics:")
    print(f"R² Score: {r2:.4f}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"Estimated Accuracy: {accuracy:.2f}%")
else:
    print("\n⚠️ Not enough data to evaluate model performance.")

# ✅ Exponential function for curve fitting
def exponential(x, a, b, c):
    return a * np.exp(b * x) + c

# 📈 Combined price trend forecast
plt.figure(figsize=(12, 6))
colors = plt.cm.tab10(np.linspace(0, 1, len(shopping_df['Item'].unique())))

for idx, item in enumerate(shopping_df['Item'].unique()):
    product_data = merged_df[merged_df['Product Name'].str.contains(item, case=False, na=False)]
    product_data = product_data.dropna(subset=['Discounted Price (Rs.)', 'Unified_Date'])

    if product_data.empty or len(product_data) < 2:
        print(f"⚠️ Not enough data to plot trend for: {item}")
        continue

    product_data = product_data.sort_values('Unified_Date')
    product_data['Days'] = (product_data['Unified_Date'] - product_data['Unified_Date'].min()).dt.days

    x = product_data['Days'].values
    y = product_data['Discounted Price (Rs.)'].values

    try:
        popt, _ = curve_fit(exponential, x, y, maxfev=10000)
        x_fit = np.linspace(min(x), max(x) + 30, 100)
        y_fit = exponential(x_fit, *popt)
        future_dates = product_data['Unified_Date'].min() + pd.to_timedelta(x_fit, unit='D')

        # Plot actual and forecast
        plt.plot(product_data['Unified_Date'], y, 'o', color=colors[idx], label=f"{item} - Actual")
        plt.plot(future_dates, y_fit, '--', color=colors[idx], label=f"{item} - Forecast")

    except Exception as e:
        print(f"❌ Curve fitting error for '{item}': {e}")

# Finalize and show/save the plot
plt.title("📈 Combined Price Forecast for All Products")
plt.xlabel("Date")
plt.ylabel("Discounted Price (Rs.)")
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# ✅ Save the graph as image
plt.savefig("price_forecast.png")
print("\n🖼️ Forecast image saved as: price_forecast.png")
plt.show()
