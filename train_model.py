import pandas as pd # type: ignore
import numpy as np # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.ensemble import RandomForestRegressor  # type: ignore # Example model
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score # type: ignore
import joblib  # type: ignore # For saving the model

# Load the dataset
cleaned_csv_path = 'cleaned_dataset_for_model.csv'
data = pd.read_csv(cleaned_csv_path, low_memory=False)

# Preprocess the data
if 'Product_Name_Combined' in data.columns:
    data = data.rename(columns={"Product_Name_Combined": "Product Name"})

# Ensure numeric columns are properly formatted
data['Discounted Price (Rs.)'] = pd.to_numeric(data.get('Discounted Price (Rs.)'), errors='coerce')
data['Original Price (Rs.)'] = pd.to_numeric(data.get('Original Price (Rs.)'), errors='coerce')

# Drop rows with missing values
data = data.dropna(subset=['Discounted Price (Rs.)', 'Original Price (Rs.)'])

# Define features (X) and target (y)
X = data[['Original Price (Rs.)']]  # Example: Use original price as the feature
y = data['Discounted Price (Rs.)']  # Target: Discounted price

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

print(f"Model Evaluation Metrics:")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")
print(f"Root Mean Squared Error (RMSE): {rmse}")
print(f"R² Score: {r2*100}")

# Save the trained model to a file
joblib.dump(model, 'trained_model.pkl', compress=3)
print("Model saved to 'trained_model.pkl'")