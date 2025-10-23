class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __str__(self):
        return f"{self.value} of {self.suit}"
        
    def get_numeric_value(self):
        if self.value == "A":
            return 14
        elif self.value == "K":
            return 13
        elif self.value == "Q":
            return 12
        elif self.value == "J":
            return 11
        else:
            return int(self.value)