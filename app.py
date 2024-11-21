from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Helper function to calculate current month's total spending
def get_current_month_spending():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Get the current month and year
    current_month = datetime.now().strftime("%Y-%m")
    cursor.execute('''
    SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = ?
    ''', (current_month,))
    total = cursor.fetchone()[0]
    connection.close()

    return total if total else 0

# Route: Homepage
@app.route('/')
def index():
    total_spending = get_current_month_spending()
    return render_template('index.html', total_spending=total_spending)

# Route: Add Expense
@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        date = request.form['date']

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute('''
        INSERT INTO expenses (description, amount, date)
        VALUES (?, ?, ?)
        ''', (description, amount, date))

        connection.commit()
        connection.close()
        return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)