import random

class Craps:
    def __init__(self):
        # Initialize dice values
        self.die1 = 0
        self.die2 = 0

    def dice1(self):
        # Generate a random value for die1
        self.die1 = random.randint(1, 6)
        return self.die1

    def dice2(self):
        # Generate a random value for die2
        self.die2 = random.randint(1, 6)
        return self.die2

    def face(self):
        diceface = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
        return diceface[self.die1], diceface[self.die2]

    def roll_dice(self):
        # Roll both dice and return their values
        self.dice1()
        self.dice2()
        return self.die1, self.die2

    def score(self):
        # Calculate the score based on the sum of the rolled dice
        return self.die1 + self.die2
