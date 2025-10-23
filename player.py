class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        
    def draw(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)
            
    def show_hand(self):
        print(f"\n{self.name}'s hand:")
        for card in self.hand:
            print(f"- {card}")