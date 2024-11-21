import sqlite3

# Initialize the database
def init_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Create table for expenses
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()