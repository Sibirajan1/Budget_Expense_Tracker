from flask import Flask, request, render_template, jsonify
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Sample dataset for price history
price_data = {
    "Milk": [2.5, 2.7, 2.6, 2.8, 2.9],
    "Bread": [1.5, 1.4, 1.6, 1.7, 1.8]
}
df = pd.DataFrame(price_data)

# Price prediction function using Linear Regression
def predict_prices(item):
    X = np.arange(len(df[item])).reshape(-1, 1)
    y = np.array(df[item])
    model = LinearRegression()
    model.fit(X, y)
    next_week_price = model.predict([[len(df[item])]])[0]
    return round(next_week_price, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        location = request.form["location"]
        items = request.form.getlist("items[]")  # User's shopping list

        total_price = sum(df[item].iloc[-1] for item in items)
        min_price = min(df[item].iloc[-1] for item in items)
        max_price = max(df[item].iloc[-1] for item in items)
        weekly_prediction = {item: predict_prices(item) for item in items}

        return jsonify({
            "total_price": total_price,
            "min_price": min_price,
            "max_price": max_price,
            "weekly_prediction": weekly_prediction
        })

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
