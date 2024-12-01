import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import game_logic
import crapsDB
from wager import Wager
from numbers import Numbers

# Initialize the main window
root = tk.Tk()
root.title("Craps Game")
root.geometry("500x400")
root.configure(background="teal")

# Load images and ensure they remain in scope
try:
    chips_image = Image.open("static/images/chips.png")
    chips_image = chips_image.resize((75, 75), Image.LANCZOS)
    chips_photo = ImageTk.PhotoImage(chips_image)

    dice_image = Image.open("static/images/Dice-icon.png")
    dice_image = dice_image.resize((75, 75), Image.LANCZOS)
    dice_photo = ImageTk.PhotoImage(dice_image)
except FileNotFoundError as e:
    print(f"Image not found: {e}")
    exit()

# Add chips image to the GUI
chips_label = tk.Label(root, image=chips_photo, bg="teal")
chips_label.place(x=375, y=10)

# Initialize global variables
point = 0
roll_number = 0
bet = 0

# Initialize CrapsDB and Wager instances
cpDB = crapsDB.crapsDB()
wager = Wager()
wager.initialize_bank_record()  # Ensure the bank table has a default record
pay = Numbers(0, bet)  # Initialize the Numbers class with the current bet

# Define variables for each Checkbutton
num4_var = tk.BooleanVar()
num5_var = tk.BooleanVar()
num6_var = tk.BooleanVar()
num8_var = tk.BooleanVar()
num9_var = tk.BooleanVar()
num10_var = tk.BooleanVar()

# Function to handle checkbox selection
def on_check(num, var):
    if var.get():  # Only act if the checkbox is selected
        print(f"Checkbox {num} selected")
        process_number(num)

# Example processing function
def process_number(num):
    placeNums = []
    placeNums.append(num)
    for num in placeNums:
        print(f"Processing number {num}")

# Roll dice function
def roll_dice():
    global point, roll_number, bet

    # Roll the dice
    die1, die2 = dice.roll_dice()  # Use the game_logic.Craps class to roll dice
    roll_number += 1
    score = die1 + die2

    # Display the dice roll results in the GUI
    result_label.config(text=f"Dice rolled: {die1}, {die2}")
    score_label.config(text=f"Score: {score}")

    # Game logic: Check if we have a winner or point
    if point == 0:  # Establishing the point
        if score in [7, 11]:
            messagebox.showinfo("Craps", "You Win!")
            wager.credit_winnings(bet)  # Add winnings to balance
        elif score in [2, 3, 12]:
            messagebox.showinfo("Craps", "Craps! You Lose!")
            loss = abs(pay.payout(score=score, bet=bet))  # Calculate the absolute loss
            wager.debit_losses(loss)  # Deduct losses
        else:
            point = score  # Set the point
            point_label.config(text=f"Point: {point}")
    else:  # Playing for the point
        if score == point:
            messagebox.showinfo("Craps", "You Win!")
            win = pay.payout(score=score, bet=bet)  # Calculate payout
            wager.credit_winnings(win)  # Add winnings
            point = 0  # Reset point
            point_label.config(text="Point: 0")
        elif score == 7:
            messagebox.showinfo("Craps", "You Lose!")
            loss = abs(pay.payout(score=score, bet=bet))  # Calculate the absolute loss
            wager.debit_losses(loss)  # Deduct losses
            point = 0  # Reset point
            point_label.config(text="Point: 0")

    # Update the balance label after any balance change
    show_balance_label.config(text=f"Balance: ${wager.get_balance():.2f}")

# Function to deposit money into the bank
def bank_deposit():
    try:
        deposit_amount = float(deposit_entry.get())  # Get the deposit amount
        if deposit_amount <= 0:
            messagebox.showerror("Error", "Deposit amount must be greater than zero.")
            return
        wager.bank_deposit(deposit_amount)  # Add deposit to the bank
        messagebox.showinfo("Success", f"Deposited ${deposit_amount:.2f} into your account.")
        deposit_entry.delete(0, tk.END)  # Clear the entry field after deposit
    except ValueError:
        messagebox.showerror("Error", "Invalid deposit amount. Please enter a numeric value.")

# Function to insert a wager
def insert_wager():
    global bet
    try:
        wager_value = radio_wager.get()  # Get the wager amount from radio buttons
        bet = {1: 5, 2: 10, 3: 25}.get(wager_value, 0)

        if bet == 0:
            messagebox.showerror("Error", "Please select a wager amount.")
            return

        wager.wager_deposit(bet)  # Update wager balance
        new_balance = wager.get_balance()
        show_balance_label.config(text=f"Balance: ${new_balance:.2f}")
        messagebox.showinfo("Success", f"Placed a wager of ${bet}. Remaining balance: ${new_balance:.2f}")

    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

# Dynamic creation of Checkbuttons
checkbuttons = {
    4: (num4_var, 160),
    5: (num5_var, 190),
    6: (num6_var, 220),
    8: (num8_var, 250),
    9: (num9_var, 280),
    10: (num10_var, 310),
}
for num, (var, x) in checkbuttons.items():
    cb = tk.Checkbutton(
        root,
        text=str(num),
        variable=var,
        command=lambda n=num, v=var: on_check(n, v),
        font=("Helvetica", 10),
        bg="white",
        fg="blue",
    )
    cb.place(x=x, y=130)

# Roll Dice button with dice image
roll_button = tk.Button(
    root,
    image=dice_photo,
    text="Roll Dice",
    font=("Helvetica", 10),
    command=roll_dice,  # Call the updated roll_dice function
    compound="top",
    bg="white",
    fg="blue",
)
roll_button.place(x=200, y=170)

# Wager buttons
radio_wager = tk.IntVar()
wager_radio_button5 = tk.Radiobutton(root, text='$5', variable=radio_wager, value=1, font=("Helvetica", 10),
                                     bg="white", fg="blue")
wager_radio_button5.place(x=25, y=130)
wager_radio_button10 = tk.Radiobutton(root, text='$10', variable=radio_wager, value=2, font=("Helvetica", 10),
                                      bg="white", fg="blue")
wager_radio_button10.place(x=25, y=150)
wager_radio_button25 = tk.Radiobutton(root, text='$25', variable=radio_wager, value=3, font=("Helvetica", 10),
                                      bg="white", fg="blue")
wager_radio_button25.place(x=25, y=170)

wager_button = tk.Button(root, text="Wager", font=("Helvetica", 10), command=insert_wager, bg="white", fg="green")
wager_button.place(x=25, y=200)

# Deposit Section
deposit_entry = tk.Entry(root, font=("Helvetica", 10), width=8)
deposit_entry.place(x=30, y=300)

deposit_button = tk.Button(root, text="Deposit", font=("Helvetica", 10), command=bank_deposit, bg="white", fg="green")
deposit_button.place(x=30, y=330)

# Labels
result_label = tk.Label(root, text="Roll the dice!", font=("Helvetica", 14), bg="teal", fg="white")
result_label.pack(pady=20)

score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 12), bg="teal", fg="white")
score_label.pack(pady=10)

point_label = tk.Label(root, text="Point: 0", font=("Helvetica", 12), bg="teal", fg="white")
point_label.place(x=25, y=20)

show_balance_label = tk.Label(root, text="Balance: $0.00", font=("Helvetica", 10), bg="teal", fg="white")
show_balance_label.place(x=350, y=300)

# Create Craps game instance
dice = game_logic.Craps()

# Run the main loop
root.mainloop()
