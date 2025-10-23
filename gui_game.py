import pygame
import sys
import random
from deck import Deck
from player import Player

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
CARD_WIDTH = 100
CARD_HEIGHT = 140
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

class CardGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Card Game")
        self.clock = pygame.time.Clock()
        
        self.reset_game()
        self.font = pygame.font.Font(None, 36)
        
    def reset_game(self):
        # Initialize game components
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player("Player 1")
        self.computer = Player("Computer")
        
        # Deal initial cards
        for _ in range(5):
            self.player.draw(self.deck)
            self.computer.draw(self.deck)
        
        self.selected_card = None
        self.player_score = 0
        self.computer_score = 0
        self.played_card = None
        self.computer_played_card = None
        self.round_result = ""
        self.game_over = False
        self.winner = None
        self.round_timer = 0

    def draw_card(self, card, x, y, highlighted=False):
        # Draw card background
        color = WHITE if not highlighted else (200, 200, 255)
        pygame.draw.rect(self.screen, color, (x, y, CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(self.screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2)
        
        # Draw card content
        card_text = f"{card.value}"
        suit_text = f"{card.suit}"
        
        # Card value
        text_surface = self.font.render(card_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x + CARD_WIDTH//2, y + CARD_HEIGHT//2))
        self.screen.blit(text_surface, text_rect)
        
        # Card suit
        suit_surface = self.font.render(suit_text, True, RED if card.suit in ["Hearts", "Diamonds"] else BLACK)
        suit_rect = suit_surface.get_rect(center=(x + CARD_WIDTH//2, y + CARD_HEIGHT//4))
        self.screen.blit(suit_surface, suit_rect)

    def get_card_at_pos(self, pos):
        x, y = pos
        # Calculate card spacing and start position
        player_cards = len(self.player.hand)
        total_margin = 100
        max_total_width = WINDOW_WIDTH - total_margin
        spacing = min(20, max(5, (max_total_width - (player_cards * CARD_WIDTH)) / (player_cards - 1) if player_cards > 1 else 0))
        
        # Calculate start position to center the cards
        total_cards_width = (CARD_WIDTH * player_cards) + (spacing * (player_cards - 1) if player_cards > 1 else 0)
        start_x = (WINDOW_WIDTH - total_cards_width) // 2
        
        for i, card in enumerate(self.player.hand):
            card_x = start_x + i * (CARD_WIDTH + spacing)
            card_y = WINDOW_HEIGHT - CARD_HEIGHT - 50
            if (card_x <= x <= card_x + CARD_WIDTH and 
                card_y <= y <= card_y + CARD_HEIGHT):
                return i
        return None

    def play_round(self, player_card_index):
        if not self.game_over and self.played_card is None:
            # Player plays a card
            self.played_card = self.player.hand.pop(player_card_index)
            
            # Computer plays a random card
            computer_card_index = random.randint(0, len(self.computer.hand) - 1)
            self.computer_played_card = self.computer.hand.pop(computer_card_index)
            
            # Compare cards and update scores
            player_value = self.played_card.get_numeric_value()
            computer_value = self.computer_played_card.get_numeric_value()
            
            if player_value > computer_value:
                self.player_score += 1
                self.round_result = "Player wins the round!"
            elif computer_value > player_value:
                self.computer_score += 1
                self.round_result = "Computer wins the round!"
            else:
                self.round_result = "It's a tie!"
            
            self.round_timer = 120  # Show result for 2 seconds (60 FPS * 2)
            
            # Check for game over
            if len(self.player.hand) == 0 or len(self.computer.hand) == 0:
                self.game_over = True
                if self.player_score > self.computer_score:
                    self.winner = "Player wins the game!"
                elif self.computer_score > self.player_score:
                    self.winner = "Computer wins the game!"
                else:
                    self.winner = "The game is a tie!"

    def run(self):
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    card_index = self.get_card_at_pos(event.pos)
                    if card_index is not None:
                        self.selected_card = card_index
                elif event.type == pygame.MOUSEBUTTONUP and not self.game_over:
                    if self.selected_card is not None:
                        self.play_round(self.selected_card)
                    self.selected_card = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()
                    elif event.key == pygame.K_SPACE and not self.game_over and self.played_card is None:
                        if len(self.deck.cards) > 0:
                            self.player.draw(self.deck)
                            self.computer.draw(self.deck)

            # Clear screen
            self.screen.fill(GREEN)

            # Calculate card spacing based on window width and number of cards
            player_cards = len(self.player.hand)
            computer_cards = len(self.computer.hand)
            max_cards = max(player_cards, computer_cards)
            
            # Calculate maximum card width that will fit
            total_margin = 100  # 50px margin on each side
            max_total_width = WINDOW_WIDTH - total_margin
            spacing = min(20, max(5, (max_total_width - (max_cards * CARD_WIDTH)) / (max_cards - 1) if max_cards > 1 else 0))
            
            # Adjust start position to center the cards
            total_cards_width = (CARD_WIDTH * player_cards) + (spacing * (player_cards - 1) if player_cards > 1 else 0)
            start_x = (WINDOW_WIDTH - total_cards_width) // 2

            # Draw player's cards
            for i, card in enumerate(self.player.hand):
                x = start_x + i * (CARD_WIDTH + spacing)
                y = WINDOW_HEIGHT - CARD_HEIGHT - 50
                self.draw_card(card, x, y, i == self.selected_card)

            # Calculate computer cards start position
            total_cards_width = (CARD_WIDTH * computer_cards) + (spacing * (computer_cards - 1) if computer_cards > 1 else 0)
            start_x = (WINDOW_WIDTH - total_cards_width) // 2

            # Draw computer's cards (face down)
            for i in range(computer_cards):
                x = start_x + i * (CARD_WIDTH + spacing)
                y = 50
                pygame.draw.rect(self.screen, RED, (x, y, CARD_WIDTH, CARD_HEIGHT))
                pygame.draw.rect(self.screen, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2)

            # Draw center played cards
            if self.played_card:
                center_y = WINDOW_HEIGHT // 2
                self.draw_card(self.played_card, WINDOW_WIDTH//2 - CARD_WIDTH - 10, center_y)
                if self.computer_played_card:
                    self.draw_card(self.computer_played_card, WINDOW_WIDTH//2 + 10, center_y)

            # Draw scores
            score_text = f"Score - Player: {self.player_score}  Computer: {self.computer_score}"
            score_surface = self.font.render(score_text, True, WHITE)
            self.screen.blit(score_surface, (20, WINDOW_HEIGHT//2 - 50))

            # Draw round result
            if self.round_timer > 0:
                result_surface = self.font.render(self.round_result, True, WHITE)
                self.screen.blit(result_surface, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 100))
                self.round_timer -= 1
                if self.round_timer == 0:
                    self.played_card = None
                    self.computer_played_card = None

            # Draw game over message
            if self.game_over:
                game_over_text = self.winner
                replay_text = "Press R to play again"
                game_over_surface = self.font.render(game_over_text, True, WHITE)
                replay_surface = self.font.render(replay_text, True, WHITE)
                self.screen.blit(game_over_surface, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 50))
                self.screen.blit(replay_surface, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 50))
            else:
                # Draw instructions
                if self.played_card is None:
                    instructions = self.font.render("Click a card to play it - Press SPACE to draw cards", True, WHITE)
                    self.screen.blit(instructions, (WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//2 - 150))

            # Update display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = CardGame()
    game.run()