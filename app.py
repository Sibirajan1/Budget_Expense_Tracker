from flask import Flask, render_template, request, redirect, session, send_file, flash
import matplotlib.pyplot as plt
import io
import joblib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
model = joblib.load('trained_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_budget', methods=['POST'])
def set_budget():
    session['budget'] = float(request.form['budget'])
    session['shopping_list'] = []
    return redirect('/add_item')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    shopping_list = session.get('shopping_list', [])
    if request.method == 'POST':
        item_name = request.form['item_name']
        quantity = int(request.form['quantity'])

        min_price = 10
        max_price = 100
        predicted_price = model.predict([[50]])[0]  # Replace 50 with actual logic
        total_price = round(predicted_price * quantity, 2)

        shopping_list.append({
            'item_name': item_name,
            'quantity': quantity,
            'min_price': min_price,
            'max_price': max_price,
            'total_price': total_price
        })
        session['shopping_list'] = shopping_list

    return render_template('add_item.html', shopping_list=shopping_list)

@app.route('/calculate')
def calculate():
    shopping_list = session.get('shopping_list', [])
    total_predicted_bill = sum(item['total_price'] for item in shopping_list)
    budget = session.get('budget', 0)

    if total_predicted_bill < budget:
        budget_message = f"\u2705 Good news! Your estimated bill of Rs. {total_predicted_bill:.2f} is within your budget of Rs. {budget:.2f}. You can comfortably buy everything on your list and still have some money left!"
        show_remove_button = False
    elif total_predicted_bill == budget:
        budget_message = f"\u2696\ufe0f Perfect match! Your estimated bill is exactly Rs. {total_predicted_bill:.2f}, which is equal to your budget. You can purchase everything on your list, but there's no margin for extras."
        show_remove_button = False
    else:
        budget_message = f"\u26a0\ufe0f Budget Alert! Your estimated bill of Rs. {total_predicted_bill:.2f} exceeds your budget of Rs. {budget:.2f}. You may need to reduce some items or quantities to stay within budget."
        show_remove_button = True

    return render_template('calculate.html', shopping_list=shopping_list,
                           total_predicted_bill=total_predicted_bill,
                           budget_message=budget_message,
                           show_remove_button=show_remove_button)

@app.route('/plot')
def plot():
    shopping_list = session.get('shopping_list', [])
    labels = [item['item_name'] for item in shopping_list]
    sizes = [item['total_price'] for item in shopping_list]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("Item Contribution to Total Cost")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/remove_item', methods=['GET', 'POST'])
def remove_item():
    shopping_list = session.get('shopping_list', [])
    if request.method == 'POST':
        updated = False
        new_list = []
        for item in shopping_list:
            item_name = item['item_name']
            check = f"check_{item_name}"
            reduce = f"decrease_{item_name}"
            if check in request.form:
                new_qty = request.form.get(reduce)
                if new_qty:
                    new_qty = int(new_qty)
                    if 0 < new_qty < item['quantity']:
                        item['quantity'] -= new_qty
                        item['total_price'] = round(item['total_price'] * (item['quantity'] / (item['quantity'] + new_qty)), 2)
                        updated = True
            new_list.append(item)

        if not updated:
            flash("⚠️ No changes made. Please select items or adjust quantity.")
            return redirect('/remove_item')

        session['shopping_list'] = new_list
        return redirect('/calculate')

    total_predicted_bill = sum(item['total_price'] for item in shopping_list)
    return render_template('remove_item.html', shopping_list=shopping_list,
                           total_predicted_bill=total_predicted_bill)

if __name__ == '__main__':
    app.run(debug=True)
