import game_logic
import crapsDB
import tkinter as tk
from tkinter import messagebox

# Initialize the main window
root = tk.Tk()
root.title("Craps Game")
root.geometry("500x400")
root.configure(background="teal")

# Initialize global variables
point = 0
roll_number = 0

# Create CrapsDB instance
cpDB = crapsDB.crapsDB()

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
    global point, roll_number
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
            new_roll_flag = 1
        elif score in [2, 3, 12]:
            messagebox.showinfo("Craps", "Craps! You Lose!")
            new_roll_flag = 1
        else:
            point = score
            point_label.config(text=f"Point: {point}")
    else:
        if score == point:
            messagebox.showinfo("Craps", "You Win!")
            point = 0
            point_label.config(text="Point: 0")
            new_roll_flag = 1
        elif score == 7:
            messagebox.showinfo("Craps", "You Lose!")
            point = 0
            point_label.config(text="Point: 0")
            new_roll_flag = 1

    # Log the roll to the database
    log_roll_to_database(point, roll_number, score, new_roll_flag)

# Function to show the dice faces
def show_face():
    face1, face2 = dice.face()
    face_label.config(text=f"Face: {face1}, {face2}")

# Create menu bar
my_menu = tk.Menu(root)
root.config(menu=my_menu)

file_menu = tk.Menu(my_menu, tearoff=0)
file_menu.add_command(label="Exit", command=lambda: (cpDB.close(), root.quit()))
file_menu.add_command(label="New Game", command=new_game)
file_menu.add_command(label="Print All Records", command=cpDB.print_all_records)
my_menu.add_cascade(label="File", menu=file_menu)

# Create an instance of the Craps class
dice = game_logic.Craps()

# Labels for the GUI
result_label = tk.Label(root, text="Roll the dice!", font=("Helvetica", 16), bg="teal", fg="white")
result_label.pack(pady=20)

score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 14), bg="teal", fg="white")
score_label.pack(pady=10)

point_label = tk.Label(root, text="Point: 0", font=("Helvetica", 14), bg="teal", fg="white")
point_label.place(x=25, y=20)

face_label = tk.Label(root, text="Face:", font=("Helvetica", 14), bg="teal", fg="white")
face_label.place(x=25, y=50)

# Roll Dice button
roll_button = tk.Button(root, text="Roll Dice", font=("Helvetica", 14), command=roll_dice, bg="white", fg="black")
roll_button.pack(pady=20)

# Run the GUI main loop
root.mainloop()
