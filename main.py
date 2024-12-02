import tkinter as tk
from tkinter import messagebox
from tkinter import Menu
from PIL import Image, ImageTk
import game_logic
import crapsDB
from wager import Wager
from numbers import Numbers


class CrapsGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Craps Game")
        self.root.geometry("500x400")
        self.root.configure(background="teal")

        # Initialize other attributes and setup GUI
        self.point = 0
        self.roll_number = 0
        self.bet = 0

        self.cpDB = crapsDB.crapsDB()
        self.wager = Wager()
        self.wager.initialize_bank_record()
        self.wager.initialize_roll_history()  # Initialize roll history table
        self.pay = Numbers(0, self.bet)
        self.dice = game_logic.Craps()

        self.num_vars = {
            4: tk.BooleanVar(),
            5: tk.BooleanVar(),
            6: tk.BooleanVar(),
            8: tk.BooleanVar(),
            9: tk.BooleanVar(),
            10: tk.BooleanVar(),
        }

        self.radio_wager = tk.IntVar()

        # Set up the GUI
        self.setup_menu()
        self.setup_images()
        self.setup_widgets()

    def update_balance_label(self):
        """Retrieve the latest balance from the database and update the GUI label."""
        balance = self.wager.get_balance()
        self.show_balance_label.config(text=f"Balance: ${balance:.2f}")

    def setup_menu(self):
        """Set up the menu with options for New Game, Show Database, and Show Roll History."""
        menu_bar = Menu(self.root)

        # File Menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Game", command=self.new_game)
        file_menu.add_command(label="Show Database", command=self.show_database)
        file_menu.add_command(label="Show Roll History", command=self.show_roll_history)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Configure the menu bar
        self.root.config(menu=menu_bar)

    def setup_images(self):
        try:
            self.chips_photo = self.load_image("static/images/chips.png", (75, 75))
            self.dice_photo = self.load_image("static/images/Dice-icon.png", (75, 75))
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Image not found: {e}")
            self.root.quit()

    @staticmethod
    def load_image(path, size):
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def setup_widgets(self):
        # Images
        tk.Label(self.root, image=self.chips_photo, bg="teal").place(x=375, y=10)

        # Labels
        self.result_label = tk.Label(self.root, text="Roll the dice!", font=("Helvetica", 14), bg="teal", fg="white")
        self.result_label.pack(pady=20)

        self.score_label = tk.Label(self.root, text="Score: 0", font=("Helvetica", 12), bg="teal", fg="white")
        self.score_label.pack(pady=10)

        self.point_label = tk.Label(self.root, text="Point: 0", font=("Helvetica", 12), bg="teal", fg="white")
        self.point_label.place(x=25, y=20)

        self.show_balance_label = tk.Label(self.root, text="Balance: $0.00", font=("Helvetica", 10), bg="teal", fg="white")
        self.show_balance_label.place(x=350, y=300)

        # Checkbuttons for numbers
        for num, x in zip(self.num_vars.keys(), range(160, 320, 30)):
            cb = tk.Checkbutton(
                self.root,
                text=str(num),
                variable=self.num_vars[num],
                command=lambda n=num: self.on_check(n),
                font=("Helvetica", 10),
                bg="white",
                fg="blue",
            )
            cb.place(x=x, y=130)

        # Roll Dice button
        tk.Button(
            self.root,
            image=self.dice_photo,
            text="Roll Dice",
            font=("Helvetica", 10),
            command=self.roll_dice,
            compound="top",
            bg="white",
            fg="blue",
        ).place(x=200, y=170)

        # Wager buttons
        for val, amount, y in zip([1, 2, 3], [5, 10, 25], [130, 150, 170]):
            tk.Radiobutton(
                self.root,
                text=f'${amount}',
                variable=self.radio_wager,
                value=val,
                font=("Helvetica", 10),
                bg="white",
                fg="blue",
            ).place(x=25, y=y)

        tk.Button(
            self.root,
            text="Wager",
            font=("Helvetica", 10),
            command=self.insert_wager,
            bg="white",
            fg="green",
        ).place(x=25, y=200)

        # Deposit Section
        self.deposit_entry = tk.Entry(self.root, font=("Helvetica", 10), width=8)
        self.deposit_entry.place(x=30, y=300)

        tk.Button(
            self.root,
            text="Deposit",
            font=("Helvetica", 10),
            command=self.bank_deposit,
            bg="white",
            fg="green",
        ).place(x=30, y=330)

    def new_game(self):
        """Reset the game state."""
        self.point = 0
        self.roll_number = 0
        self.bet = 0
        self.update_balance_label()
        self.point_label.config(text="Point: 0")
        self.score_label.config(text="Score: 0")
        self.result_label.config(text="Roll the dice!")
        messagebox.showinfo("New Game", "Game reset! You can start a new game.")

    def show_database(self):
        """Retrieve and print all data in the bank table."""
        try:
            data = self.wager.cursor.execute("SELECT * FROM bank").fetchall()
            if data:
                print("Database Records:")
                for row in data:
                    print(row)

                records = "\n".join([str(row) for row in data])
                messagebox.showinfo("Database Records", f"Data in the database:\n{records}")
            else:
                messagebox.showinfo("Database Records", "No data available in the database.")
        except Exception as e:
            print(f"Error retrieving database records: {e}")
            messagebox.showerror("Error", f"Failed to retrieve database records: {e}")

    def show_roll_history(self):
        """Retrieve and display all roll history records."""
        try:
            data = self.wager.cursor.execute("SELECT * FROM roll_history ORDER BY id DESC").fetchall()
            if data:
                print("Roll History:")
                for row in data:
                    print(row)

                records = "\n".join([f"Roll {row[1]}: {row[2]}, {row[3]} (Score: {row[4]}) - {row[5]}" for row in data])
                messagebox.showinfo("Roll History", f"Rolls:\n{records}")
            else:
                messagebox.showinfo("Roll History", "No rolls recorded yet.")
        except Exception as e:
            print(f"Error retrieving roll history: {e}")
            messagebox.showerror("Error", f"Failed to retrieve roll history: {e}")

    def on_check(self, num):
        if self.num_vars[num].get():
            print(f"Checkbox {num} selected")
            self.process_number(num)

    @staticmethod
    def process_number(num):
        print(f"Processing number {num}")

    def roll_dice(self):
        self.roll_number += 1  # Increment roll number
        die1, die2 = self.dice.roll_dice()
        score = die1 + die2

        # Log the roll to the database
        self.wager.log_roll(self.roll_number, die1, die2, score)

        # Update the GUI with roll results
        self.result_label.config(text=f"Dice rolled: {die1}, {die2}")
        self.score_label.config(text=f"Score: {score}")

        # Handle game logic
        if self.point == 0:
            self.handle_initial_roll(score)
        else:
            self.handle_point_roll(score)

        # Update balance display
        self.update_balance_label()

    def handle_initial_roll(self, score):
        if score in [7, 11]:
            messagebox.showinfo("Craps", "You Win!")
            self.wager.credit_winnings(self.bet)
        elif score in [2, 3, 12]:
            messagebox.showinfo("Craps", "Craps! You Lose!")
            loss = self.bet
            print(f"Losing {loss}. Debiting from balance.")  # Debugging
            self.wager.debit_losses(loss)
            self.update_balance_label()
        else:
            self.point = score
            self.point_label.config(text=f"Point: {self.point}")

    def handle_point_roll(self, score):
        if score == self.point:
            messagebox.showinfo("Craps", "You Win!")
            win = self.pay.payout(score=score, bet=self.bet)
            self.wager.credit_winnings(win)
            self.reset_point()
        elif score == 7:
            messagebox.showinfo("Craps", "You Lose!")
            loss = self.bet
            print(f"Losing {loss}. Debiting from balance.")  # Debugging
            self.wager.debit_losses(loss)
            self.update_balance_label()
            self.reset_point()

    def update_balance_label(self):
        balance = self.wager.get_balance()
        print(f"Updated Balance: ${balance}")  # Debugging
        self.show_balance_label.config(text=f"Balance: ${balance:.2f}")

    def bank_deposit(self):
        try:
            deposit_amount = float(self.deposit_entry.get())
            if deposit_amount <= 0:
                raise ValueError("Deposit must be greater than zero.")
            self.wager.bank_deposit(deposit_amount)
            messagebox.showinfo("Success", f"Deposited ${deposit_amount:.2f} into your account.")
            self.deposit_entry.delete(0, tk.END)
            self.update_balance_label()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def insert_wager(self):
        wager_value = self.radio_wager.get()
        self.bet = {1: 5, 2: 10, 3: 25}.get(wager_value, 0)
        if self.bet <= 0:
            messagebox.showerror("Error", "Please select a valid wager amount.")
            return
        try:
            self.wager.wager_deposit(self.bet)
            messagebox.showinfo("Success", f"Placed a wager of ${self.bet}.")
            self.update_balance_label()
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = CrapsGameApp(root)  # Pass the root Tkinter object
    root.mainloop()
