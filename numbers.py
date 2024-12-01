class Numbers:
    def __init__(self, number, bet, comeout=False):
        self.number = number
        self.bet = bet
        self.comeout = comeout

    def payout(self, score=None, bet=None):
        if self.comeout:  # Handle comeout roll
            if score in (7, 11):  # Win conditions during comeout roll
                return bet * 2
            elif score in (2, 3, 12):  # Loss conditions during comeout roll
                return -bet  # Return negative for loss
            else:
                return 0  # No payout for other numbers during comeout
        else:  # Handle non-comeout roll
            # Define payout multipliers for non-comeout rolls
            payout_multipliers = {
                4: 3,
                5: 2.2,
                6: 1.75,
                8: 1.75,
                9: 2.2,
                10: 3,
            }
            # Calculate payout based on multiplier
            return bet * payout_multipliers.get(score, 0)  # Default to 0 if number is not valid
