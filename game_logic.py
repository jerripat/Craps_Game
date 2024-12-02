import random

class Craps:
    def __init__(self):
        """Initialize dice values."""
        self.die1 = 0
        self.die2 = 0

    def roll_dice(self):
        """
        Rolls both dice and returns their values.
        :return: Tuple of two integers representing the dice rolls.
        """
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        return self.die1, self.die2

    def score(self):
        """
        Calculates the score based on the sum of the rolled dice.
        :return: Integer representing the sum of die1 and die2.
        """
        return self.die1 + self.die2

    def face(self):
        """
        Returns the string representation of the dice faces.
        :return: Tuple of strings representing the dice faces.
        """
        diceface = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six'}
        return diceface.get(self.die1, 'zero'), diceface.get(self.die2, 'zero')

    def dice1(self):
        """
        Rolls the first die and returns its value.
        :return: Integer representing the value of die1.
        """
        self.die1 = random.randint(1, 6)
        return self.die1

    def dice2(self):
        """
        Rolls the second die and returns its value.
        :return: Integer representing the value of die2.
        """
        self.die2 = random.randint(1, 6)
        return self.die2
