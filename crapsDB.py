import sqlite3


class crapsDB:
    def __init__(self):
        # Initialize database connection and cursor
        self.connection = sqlite3.connect('craps_database.db')
        self.cursor = self.connection.cursor()
        self._initialize_tables()

    def _initialize_tables(self):
        # Create the craps_scores table if it doesn't exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS craps_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            point INTEGER,
            roll_number INTEGER NOT NULL,
            score INTEGER NOT NULL,
            new_roll INTEGER DEFAULT 0
        )
        ''')

        # Create the bank table if it doesn't exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS bank (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deposit REAL DEFAULT 0,
            wager REAL DEFAULT 0,
            credit REAL DEFAULT 0,
            debit REAL DEFAULT 0,
            balance REAL DEFAULT 0
        )
        ''')
        self.connection.commit()

    def insert_roll(self, point, roll_number, score, new_roll):
        # Insert a roll record into the craps_scores table
        self.cursor.execute('''
        INSERT INTO craps_scores (point, roll_number, score, new_roll)
        VALUES (?, ?, ?, ?)
        ''', (point, roll_number, score, new_roll))
        self.connection.commit()

    def insert_bank_record(self, deposit=0, wager=0, credit=0, debit=0, balance=0):
        # Insert a record into the bank table
        self.cursor.execute('''
        INSERT INTO bank (deposit, wager, credit, debit, balance)
        VALUES (?, ?, ?, ?, ?)
        ''', (deposit, wager, credit, debit, balance))
        self.connection.commit()

    def get_all_data(self, table_name):
        # Retrieve all data from the specified table
        self.cursor.execute(f'SELECT * FROM {table_name}')
        return self.cursor.fetchall()

    def print_all_records(self, table_name):
        # Print all records from the specified table
        records = self.get_all_data(table_name)
        for record in records:
            print(record)

    def close(self):
        # Close the database connection
        if self.connection:
            self.connection.close()
