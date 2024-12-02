import sqlite3


class Wager:
    def __init__(self):
        try:
            # Establish connection to the database
            self.conn = sqlite3.connect('craps_database.db')
            self.cursor = self.conn.cursor()
            self.initialize_bank_record()
            self.initialize_roll_history()  # Initialize roll history table
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def initialize_bank_record(self):
        try:
            # Initialize the bank table with a default record if it doesn't exist
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS bank (
                    id INTEGER PRIMARY KEY,
                    deposit REAL DEFAULT 0,
                    wager REAL DEFAULT 0,
                    credit REAL DEFAULT 0,
                    debit REAL DEFAULT 0,
                    balance REAL DEFAULT 0
                )
            """)
            self.cursor.execute("SELECT COUNT(*) FROM bank WHERE id = 1")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute("""
                    INSERT INTO bank (id, deposit, wager, credit, debit, balance)
                    VALUES (1, 0, 0, 0, 0, 0)
                """)
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing bank table: {e}")
            raise

    def initialize_roll_history(self):
        """Create the roll_history table if it doesn't exist."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS roll_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_number INTEGER,
                    die1 INTEGER,
                    die2 INTEGER,
                    score INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing roll history table: {e}")
            raise

    def log_roll(self, roll_number, die1, die2, score):
        """Insert a roll into the roll_history table."""
        try:
            self.cursor.execute("""
                INSERT INTO roll_history (roll_number, die1, die2, score)
                VALUES (?, ?, ?, ?)
            """, (roll_number, die1, die2, score))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error logging roll: {e}")
            raise

    def bank_deposit(self, deposit):
        if deposit <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        try:
            self.cursor.execute("""
                UPDATE bank
                SET deposit = deposit + ?, balance = deposit + ?
                WHERE id = 1
            """, (deposit, deposit))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating deposit: {e}")
            raise

    def get_deposit(self):
        try:
            self.cursor.execute("SELECT deposit FROM bank WHERE id = 1")
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Error retrieving deposit: {e}")
            raise

    def get_balance(self):
        try:
            self.cursor.execute("SELECT balance FROM bank WHERE id = 1")
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Error retrieving balance: {e}")
            raise

    def wager_deposit(self, wager):
        if wager <= 0:
            raise ValueError("Wager amount must be greater than zero.")
        try:
            self.cursor.execute("BEGIN TRANSACTION")
            self.cursor.execute("SELECT deposit FROM bank WHERE id = 1")
            deposit = self.cursor.fetchone()[0]
            if deposit < wager:
                raise ValueError("Insufficient funds for this wager.")
            self.cursor.execute("""
                UPDATE bank
                SET deposit = deposit - ?, wager = wager + ?, balance = deposit - ?
                WHERE id = 1
            """, (wager, wager, wager))
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Error processing wager: {e}")
            raise

    def credit_winnings(self, winnings):
        if winnings < 0:
            raise ValueError("Winnings must be non-negative.")
        try:
            self.cursor.execute("""
                UPDATE bank
                SET credit = credit + ?, balance = balance + ?
                WHERE id = 1
            """, (winnings, winnings))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error crediting winnings: {e}")
            raise

    def debit_losses(self, losses):
        if losses < 0:
            raise ValueError("Losses must be non-negative.")
        try:
            self.cursor.execute("""
                UPDATE bank
                SET debit = debit + ?, balance = balance - ?
                WHERE id = 1
            """, (losses, losses))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error debiting losses: {e}")
            raise

    def close(self):
        # Close the database connection
        if self.conn:
            self.conn.close()
            self.conn = None
