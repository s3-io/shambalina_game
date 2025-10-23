from deck import Deck
from player import Player

def main():
    # Create a new deck and shuffle it
    deck = Deck()
    deck.shuffle()
    
    # Create players
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    
    # Each player draws 5 cards
    for _ in range(5):
        player1.draw(deck)
        player2.draw(deck)
    
    # Show players' hands
    player1.show_hand()
    player2.show_hand()

if __name__ == "__main__":
    main()