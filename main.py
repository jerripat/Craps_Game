import game_logic
import crapsDB
from numbers import Numbers
from wager import Wager  # Import the Wager class
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Initialize the main window
root = tk.Tk()
root.title("Craps Game")
root.geometry("500x400")
root.configure(background="teal")


try:
    image = Image.open("static/images/chips.png")  # Ensure chips.png is in the same directory
    image = image.resize((75, 75), Image.LANCZOS)  # Resize as necessary
    photo = ImageTk.PhotoImage(image)
except FileNotFoundError:
    print("chips.png not found. Ensure the file is in the correct directory.")
    exit()

# Add the image to the form
image_label = tk.Label(root, image=photo)
image_label.place(x=375,y=10) # Display the image
# Initialize global variables
point = 0
roll_number = 0

# Initialize CrapsDB instance
cpDB = crapsDB.crapsDB()

# Initialize Wager instance
wager = Wager()
wager.initialize_bank_record()  # Ensure the bank table has a default record
 # initialize the betting variable
bet = 0


# Variables for each Checkbutton
num4_var = tk.IntVar()
num5_var = tk.IntVar()
num6_var = tk.IntVar()
num8_var = tk.IntVar()
num9_var = tk.IntVar()
num10_var = tk.IntVar()

# Define the callback function
def on_check():
    print(f"4: {'Selected' if num4_var.get() else 'Deselected'}")
    print(f"5: {'Selected' if num5_var.get() else 'Deselected'}")
    print(f"6: {'Selected' if num6_var.get() else 'Deselected'}")
    print(f"8: {'Selected' if num8_var.get() else 'Deselected'}")
    print(f"9: {'Selected' if num9_var.get() else 'Deselected'}")
    print(f"10: {'Selected' if num10_var.get() else 'Deselected'}")





# Function to start a new game
def new_game():
    global point, roll_number
    dice.die1 = 0
    dice.die2 = 0
    result_label.config(text="Roll the dice!")
    score_label.config(text="Score: 0")
    point_label.config(text="Point: 0")
    face_label.config(text="Face:")
    point = 0
    roll_number = 0


# Function to log roll data to the database
def log_roll_to_database(point, roll_number, score, new_roll):
    cpDB.insert_roll(point, roll_number, score, new_roll)


# Function to roll the dice
def roll_dice():
    global point, roll_number, bet
    roll_number += 1
    die1, die2 = dice.roll_dice()
    score = dice.score()
    new_roll_flag = 0

    # Update GUI with dice roll results
    result_label.config(text=f"Dice rolled: {die1}, {die2}")
    score_label.config(text=f"Score: {score}")
    show_face()  # Update dice faces

    if point == 0:
        if score == 7 or score == 11:
            messagebox.showinfo("Craps", "You Win!")
            wager.credit_winnings(bet)  # Add winnings to the credit
            show_balance_label.config(text=f"Balance: ${wager.get_balance():.2f}")
            new_roll_flag = 1
        elif score in [2, 3, 12]:
            messagebox.showinfo("Craps", "Craps! You Lose!")
            wager.debit_losses(bet)  # Subtract losses from the debit
            show_balance_label.config(text=f"Balance: ${wager.get_balance():.2f}")
            new_roll_flag = 1
        else:
            point = score
            point_label.config(text=f"Point: {point}")
    else:
        if score == point:
            messagebox.showinfo("Craps", "You Win!")
            wager.credit_winnings(bet)  # Add winnings to the credit
            show_balance_label.config(text=f"Balance: ${wager.get_balance():.2f}")
            point = 0
            point_label.config(text="Point: 0")
            new_roll_flag = 1
        elif score == 7:
            messagebox.showinfo("Craps", "You Lose!")
            wager.debit_losses(bet)  # Subtract losses from the debit
            show_balance_label.config(text=f"Balance: ${wager.get_balance():.2f}")
            point = 0
            point_label.config(text="Point: 0")
            new_roll_flag = 1

    # Log the roll to the database
    log_roll_to_database(point, roll_number, score, new_roll_flag)


# Function to show the dice faces
def show_face():
    face1, face2 = dice.face()
    face_label.config(text=f"Face: {face1}, {face2}")


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


# Function to show current deposit
def show_deposit():
    try:
        deposit = wager.get_deposit()  # Get the current deposit from the database
        messagebox.showinfo("Current Deposit", f"Your current deposit is: ${deposit:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch deposit: {str(e)}")


def insert_wager():
    global bet
    try:
        # Get the wager amount based on the selected radio button
        wager_value = radio_wager.get()  # Get the value from the radio button group

        # Map radio button values to wager amounts
        bet = {1: 5, 2: 10, 3: 25}.get(wager_value, 0)

        if bet == 0:
            messagebox.showerror("Error", "Please select a wager amount.")
            return

        # Place the wager and update the balance
        wager.wager_deposit(bet)
        new_balance = wager.get_balance()

        # Update the balance label
        show_balance_label.config(text=f"Balance: ${new_balance:.2f}")
        messagebox.showinfo("Success", f"Placed a wager of ${bet}. Remaining balance: ${new_balance:.2f}")

    except ValueError as e:
        messagebox.showerror("Error", f"Failed to place wager: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")


# Create menu bar
my_menu = tk.Menu(root)
root.config(menu=my_menu)

file_menu = tk.Menu(my_menu, tearoff=0)
file_menu.add_command(label="Exit", command=lambda: (cpDB.close(), wager.close(), root.quit()))
file_menu.add_command(label="New Game", command=new_game)
file_menu.add_command(label="Print Records", command=lambda: cpDB.print_all_records('craps_scores'))
file_menu.add_command(label="Show Deposits", command=show_deposit)
my_menu.add_cascade(label="File", menu=file_menu)

# Create an instance of the Craps class
dice = game_logic.Craps()
radio_wager = tk.IntVar()
wager_radio_button5 = tk.Radiobutton(root, text=' $5', width=5, variable=radio_wager, value=1, font=("Helvetica", 10),
                                     bg="white", fg="blue")
wager_radio_button5.place(x=25, y=130)
wager_radio_button10 = tk.Radiobutton(root, text='$10', width=5, variable=radio_wager, value=2, font=("Helvetica", 10),
                                      bg="white", fg="blue")
wager_radio_button10.place(x=25, y=150)
wager_radio_button25 = tk.Radiobutton(root, text='$25', width=5, variable=radio_wager, value=3, font=("Helvetica", 10),
                                      bg="white", fg="blue")
wager_radio_button25.place(x=25, y=170)
# Labels for the GUI
result_label = tk.Label(root, text="Roll the dice!", font=("Helvetica", 14), bg="teal", fg="white")
result_label.pack(pady=20)

wager_label = tk.Label(root, text="Wager:", font=("Helvetica", 10), bg="teal", fg="white")
wager_label.place(x=25, y=110)

wager_button = tk.Button(root, text="Wager", font=("Helvetica", 10), command=insert_wager, bg="white", fg="green")
wager_button.place(x=25, y=200)

score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 12), bg="teal", fg="white")
score_label.pack(pady=10)

point_label = tk.Label(root, text="Point: 0", font=("Helvetica", 12), bg="teal", fg="white")
point_label.place(x=25, y=20)

face_label = tk.Label(root, text="Face:", font=("Helvetica", 12), bg="teal", fg="white")
face_label.place(x=25, y=50)


try:
    image = Image.open("static/images/Dice-icon.png")  # Replace with your image path
    image = image.resize((75, 75), Image.LANCZOS)  # Resize the image if needed
    photo1 = ImageTk.PhotoImage(image)
except FileNotFoundError:
    print("Image not found. Make sure 'chips.png' is in the same directory.")
    exit()
# Roll Dice button
roll_button = tk.Button(root, image=photo1, text="Roll Dice", font=("Helvetica", 10), command=roll_dice, bg="white", fg="blue")
roll_button.pack(pady=95)

# Deposit Section
bank_deposit_label = tk.Label(root, text="Bank Deposit:", font=("Helvetica", 10), bg="teal", fg="white")
bank_deposit_label.place(x=25, y=280)

deposit_entry = tk.Entry(root, font=("Helvetica", 10), width=9)
deposit_entry.place(x=30, y=300)

deposit_button = tk.Button(root, text="Deposit", font=("Helvetica", 8), command=bank_deposit, bg="white", fg="green")
deposit_button.place(x=33, y=330)

balance_label = tk.Label(root, text="Bank Balance:", font=("Helvetica", 10), bg="teal", fg="white")
balance_label.place(x=350, y=280)
show_balance_label = tk.Label(root, text="Balance", font=("Helvetica", 10), bg="teal", fg="white")
show_balance_label.place(x=350, y=300)

# odds_frame = tk.Frame(root, bg="darkblue", width=200, height=50, relief=tk.RAISED)
# odds_frame.place(x=150, y=110)
# Create Checkbuttons
num4 = tk.Checkbutton(root, text="4", variable=num4_var, command=on_check, font=("Helvetica", 10), bg="white", fg="blue")
num4.place(x=160, y=130)

num5 = tk.Checkbutton(root, text="5", variable=num5_var, command=on_check, font=("Helvetica", 10), bg="white", fg="blue")
num5.place(x=190, y=130)

num6 = tk.Checkbutton(root, text="6", variable=num6_var, command=on_check, font=("Helvetica", 10), bg="white", fg="blue")
num6.place(x=220, y=130)

num8 = tk.Checkbutton(root, text="8", variable=num8_var, command=on_check, font=("Helvetica", 10), bg="white", fg="blue")
num8.place(x=250, y=130)

num9 = tk.Checkbutton(root, text="9", variable=num9_var, command=on_check, font=("Helvetica", 10), bg="white", fg="blue")
num9.place(x=280, y=130)

num10 = tk.Checkbutton(root, text="10", variable=num10_var, command=on_check, font=("Helvetica", 10), bg="white", fg="blue")
num10.place(x=310, y=130)
#

# Run the GUI main loop
root.mainloop()
