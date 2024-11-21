from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row  # Enable dict-like access to rows
    return connection

# Helper function to calculate current month's total spending
def get_current_month_spending():
    connection = get_db_connection()
    current_month = datetime.now().strftime("%Y-%m")
    cursor = connection.execute('''
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

        connection = get_db_connection()
        connection.execute('''
            INSERT INTO expenses (description, amount, date)
            VALUES (?, ?, ?)
        ''', (description, amount, date))
        connection.commit()
        connection.close()

        return redirect(url_for('index'))
    return render_template('add.html')

# Route: View All Expenses
@app.route('/view')
def view_expenses():
    connection = get_db_connection()
    expenses = connection.execute('SELECT * FROM expenses').fetchall()
    connection.close()
    return render_template('view.html', expenses=expenses)

# Route: Edit Expense
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    connection = get_db_connection()
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        date = request.form['date']

        connection.execute('''
            UPDATE expenses SET description = ?, amount = ?, date = ?
            WHERE id = ?
        ''', (description, amount, date, id))
        connection.commit()
        connection.close()
        return redirect(url_for('view_expenses'))

    expense = connection.execute('SELECT * FROM expenses WHERE id = ?', (id,)).fetchone()
    connection.close()
    return render_template('edit.html', expense=expense)

# Route: Delete Expense
@app.route('/delete/<int:id>')
def delete_expense(id):
    connection = get_db_connection()
    connection.execute('DELETE FROM expenses WHERE id = ?', (id,))
    connection.commit()
    connection.close()
    return redirect(url_for('view_expenses'))

if __name__ == '__main__':
    app.run(debug=True)