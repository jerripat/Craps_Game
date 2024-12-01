import sqlite3

class Wager:
    def __init__(self):
        # Establish connection to the database
        self.conn = sqlite3.connect('craps_database.db')
        self.cursor = self.conn.cursor()

    def bank_deposit(self, deposit):
        # Update the deposit value in the bank table
        self.cursor.execute("UPDATE bank SET deposit = deposit + ? WHERE id = 1", (deposit,))
        self.conn.commit()

    def get_deposit(self):
        # Retrieve the current deposit value from the bank table
        self.cursor.execute("SELECT deposit FROM bank WHERE id = 1")
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def get_balance(self):
        # Retrieve the current balance value from the bank table
        self.cursor.execute("SELECT balance FROM bank WHERE id = 1")
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def initialize_bank_record(self):
        # Initialize the bank table with a default record if it doesn't exist
        self.cursor.execute("SELECT COUNT(*) FROM bank WHERE id = 1")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute(
                "INSERT INTO bank (id, deposit, wager, credit, debit, balance) VALUES (1, 0, 0, 0, 0, 0)"
            )
            self.conn.commit()

    def wager_deposit(self, wager):
        # Check if the deposit is sufficient for the wager
        self.cursor.execute("SELECT deposit FROM bank WHERE id = 1")
        deposit = self.cursor.fetchone()[0]
        if deposit < wager:
            raise ValueError("Insufficient funds for this wager.")

        # Subtract the wager from the deposit and update the balance
        self.cursor.execute("UPDATE bank SET deposit = deposit - ?, wager = wager + ?, balance = deposit - ? WHERE id = 1",
                            (wager, wager, wager))
        self.conn.commit()

    def credit_winnings(self, winnings):
        # Add the winnings to the credit and update the balance
        self.cursor.execute("UPDATE bank SET credit = credit +?, balance = balance +? WHERE id = 1",
                            (winnings, winnings))
        self.conn.commit()

    def debit_losses(self, losses):
        # Subtract the losses from the debit and update the balance
        self.cursor.execute("UPDATE bank SET debit = debit +?, balance = balance -? WHERE id = 1",
                            (losses, losses))
        self.conn.commit()
    def close(self):
        # Close the database connection
        if self.conn:
            self.conn.close()
