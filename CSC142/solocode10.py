import random
import sys

import pygame


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TABLE_GREEN = (24, 120, 70)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (180, 40, 40)
BLUE = (35, 85, 190)
GOLD = (235, 195, 70)
GRAY = (220, 220, 220)


class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def get_label(self):
        suit_letters = {
            "Spades": "S",
            "Hearts": "H",
            "Diamonds": "D",
            "Clubs": "C",
        }
        return self.rank + suit_letters[self.suit]


class MovingCard:
    def __init__(self, card, x, y, target_x, target_y):
        self.card = card
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 10

    def update(self):
        if self.x < self.target_x:
            self.x += self.speed
            if self.x > self.target_x:
                self.x = self.target_x
        elif self.x > self.target_x:
            self.x -= self.speed
            if self.x < self.target_x:
                self.x = self.target_x

        if self.y < self.target_y:
            self.y += self.speed
            if self.y > self.target_y:
                self.y = self.target_y
        elif self.y > self.target_y:
            self.y -= self.speed
            if self.y < self.target_y:
                self.y = self.target_y

    def is_finished(self):
        return self.x == self.target_x and self.y == self.target_y


class SpadesGame:
    TURN_TIME = 10
    COMPUTER_WAIT = 800
    RESULT_WAIT = 1000

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Simple Spades")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont(None, 42)
        self.text_font = pygame.font.SysFont(None, 30)
        self.card_font = pygame.font.SysFont(None, 28)

        self.restart_rect = pygame.Rect(820, 20, 140, 45)
        self.reset_game()

    def reset_game(self):
        self.player_hand = []
        self.computer_hand = []
        self.player_tricks = 0
        self.computer_tricks = 0
        self.round_number = 1
        self.lead_suit = None
        self.state = "player_turn"
        self.message = "Click a card to play."
        self.turn_start_time = pygame.time.get_ticks()
        self.wait_start_time = 0
        self.result_start_time = 0

        self.player_card = None
        self.computer_card = None
        self.player_animation = None
        self.computer_animation = None

        self.make_hands()
        self.sort_hands()

    def make_hands(self):
        deck = []
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        ranks = [
            ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7),
            ("8", 8), ("9", 9), ("10", 10), ("J", 11), ("Q", 12), ("K", 13), ("A", 14),
        ]

        for suit in suits:
            for rank, value in ranks:
                deck.append(Card(suit, rank, value))

        random.shuffle(deck)
        self.player_hand = deck[:13]
        self.computer_hand = deck[13:26]

    def sort_hands(self):
        suit_order = {"Clubs": 0, "Diamonds": 1, "Hearts": 2, "Spades": 3}
        self.player_hand.sort(key=lambda card: (suit_order[card.suit], card.value))
        self.computer_hand.sort(key=lambda card: (suit_order[card.suit], card.value))

    def get_player_card_position(self, index):
        x = 35 + index * 72
        y = 560
        return x, y

    def get_legal_indexes(self, hand):
        if self.lead_suit is None:
            return list(range(len(hand)))

        matching = []
        for index, card in enumerate(hand):
            if card.suit == self.lead_suit:
                matching.append(index)

        if len(matching) > 0:
            return matching
        return list(range(len(hand)))

    def play_player_card(self, index):
        legal_indexes = self.get_legal_indexes(self.player_hand)
        if index not in legal_indexes:
            self.message = "You must follow the lead suit."
            return

        card = self.player_hand.pop(index)
        self.player_card = card

        if self.lead_suit is None:
            self.lead_suit = card.suit

        start_x, start_y = self.get_player_card_position(index)
        self.player_animation = MovingCard(card, start_x, start_y, 360, 285)
        self.state = "player_animation"
        self.message = "You played " + card.get_label()

    def play_computer_card(self):
        legal_indexes = self.get_legal_indexes(self.computer_hand)
        chosen_index = legal_indexes[0]

        for index in legal_indexes:
            if self.computer_hand[index].value < self.computer_hand[chosen_index].value:
                chosen_index = index

        card = self.computer_hand.pop(chosen_index)
        self.computer_card = card

        if self.lead_suit is None:
            self.lead_suit = card.suit

        start_x = 120 + chosen_index * 60
        start_y = 180
        self.computer_animation = MovingCard(card, start_x, start_y, 560, 285)
        self.state = "computer_animation"
        self.message = "Computer played " + card.get_label()

    def compare_cards(self):
        if self.player_card.suit == "Spades" and self.computer_card.suit != "Spades":
            return "player"
        if self.computer_card.suit == "Spades" and self.player_card.suit != "Spades":
            return "computer"

        if self.player_card.suit == self.computer_card.suit:
            if self.player_card.value >= self.computer_card.value:
                return "player"
            return "computer"

        if self.player_card.suit == self.lead_suit:
            return "player"
        return "computer"

    def score_round(self):
        winner = self.compare_cards()

        if winner == "player":
            self.player_tricks += 1
            self.message = "You won the trick."
            next_player = "player_turn"
        else:
            self.computer_tricks += 1
            self.message = "Computer won the trick."
            next_player = "computer_turn"

        self.player_card = None
        self.computer_card = None
        self.player_animation = None
        self.computer_animation = None
        self.lead_suit = None

        if len(self.player_hand) == 0:
            if self.player_tricks > self.computer_tricks:
                self.message = "Game over. You win!"
            elif self.player_tricks < self.computer_tricks:
                self.message = "Game over. Computer wins!"
            else:
                self.message = "Game over. Tie game."
            self.state = "game_over"
            return

        self.round_number += 1
        self.state = next_player
        self.turn_start_time = pygame.time.get_ticks()
        self.wait_start_time = pygame.time.get_ticks()

    def handle_player_timeout(self):
        legal_indexes = self.get_legal_indexes(self.player_hand)
        self.message = "Time ran out. A card was played for you."
        self.play_player_card(legal_indexes[0])

    def handle_mouse_click(self, mouse_pos):
        if self.restart_rect.collidepoint(mouse_pos):
            self.reset_game()
            return

        if self.state != "player_turn":
            return

        for index in range(len(self.player_hand)):
            x, y = self.get_player_card_position(index)
            card_rect = pygame.Rect(x, y, 60, 100)
            if card_rect.collidepoint(mouse_pos):
                self.play_player_card(index)
                return

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.state == "player_turn":
            seconds_used = (current_time - self.turn_start_time) / 1000
            if seconds_used >= self.TURN_TIME:
                self.handle_player_timeout()

        elif self.state == "computer_turn":
            if current_time - self.wait_start_time >= self.COMPUTER_WAIT:
                self.play_computer_card()

        elif self.state == "player_animation":
            self.player_animation.update()
            if self.player_animation.is_finished():
                self.player_animation = None
                if self.computer_card is None:
                    self.state = "computer_turn"
                    self.wait_start_time = pygame.time.get_ticks()
                    self.message = "Computer is thinking..."
                else:
                    self.state = "show_result"
                    self.result_start_time = pygame.time.get_ticks()

        elif self.state == "computer_animation":
            self.computer_animation.update()
            if self.computer_animation.is_finished():
                self.computer_animation = None
                if self.player_card is None:
                    self.state = "player_turn"
                    self.turn_start_time = pygame.time.get_ticks()
                    self.message = "Your turn. Click a card."
                else:
                    self.state = "show_result"
                    self.result_start_time = pygame.time.get_ticks()

        elif self.state == "show_result":
            if current_time - self.result_start_time >= self.RESULT_WAIT:
                self.score_round()

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.window.blit(text_surface, (x, y))

    def draw_card(self, card, x, y, face_up):
        rect = pygame.Rect(x, y, 60, 100)

        if face_up:
            pygame.draw.rect(self.window, WHITE, rect, border_radius=8)
            pygame.draw.rect(self.window, BLACK, rect, 2, border_radius=8)
            self.draw_text(card.get_label(), self.card_font, BLACK, x + 12, y + 38)
        else:
            pygame.draw.rect(self.window, BLUE, rect, border_radius=8)
            pygame.draw.rect(self.window, BLACK, rect, 2, border_radius=8)
            self.draw_text("CARD", self.card_font, WHITE, x + 8, y + 38)

    def draw_restart_button(self):
        pygame.draw.rect(self.window, GOLD, self.restart_rect, border_radius=8)
        pygame.draw.rect(self.window, BLACK, self.restart_rect, 2, border_radius=8)
        self.draw_text("Restart", self.text_font, BLACK, 855, 31)

    def draw(self):
        self.window.fill(TABLE_GREEN)

        self.draw_text("Simple Spades", self.title_font, WHITE, 20, 20)
        self.draw_text(
            "Round: " + str(self.round_number) +
            "   You: " + str(self.player_tricks) +
            "   Computer: " + str(self.computer_tricks),
            self.text_font,
            WHITE,
            20,
            75,
        )
        self.draw_text(self.message, self.text_font, GOLD, 20, 115)

        if self.state == "player_turn":
            time_left = self.TURN_TIME - ((pygame.time.get_ticks() - self.turn_start_time) / 1000)
            if time_left < 0:
                time_left = 0
            self.draw_text(f"Time Left: {time_left:.1f}", self.text_font, WHITE, 20, 155)
        elif self.state == "game_over":
            self.draw_text("Click Restart to play again.", self.text_font, WHITE, 20, 155)
        else:
            self.draw_text(" ", self.text_font, WHITE, 20, 155)

        self.draw_restart_button()
        self.draw_text("Computer", self.title_font, WHITE, 430, 130)
        self.draw_text("You", self.title_font, WHITE, 470, 660)

        for index in range(len(self.computer_hand)):
            self.draw_card(self.computer_hand[index], 120 + index * 60, 180, False)

        for index in range(len(self.player_hand)):
            x, y = self.get_player_card_position(index)
            self.draw_card(self.player_hand[index], x, y, True)

        if self.player_animation is not None:
            self.draw_card(self.player_animation.card, self.player_animation.x, self.player_animation.y, True)
        elif self.player_card is not None:
            self.draw_card(self.player_card, 360, 285, True)

        if self.computer_animation is not None:
            self.draw_card(self.computer_animation.card, self.computer_animation.x, self.computer_animation.y, True)
        elif self.computer_card is not None:
            self.draw_card(self.computer_card, 560, 285, True)

        if self.lead_suit is not None:
            self.draw_text("Lead Suit: " + self.lead_suit, self.text_font, GRAY, 430, 250)

        pygame.display.update()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)


game = SpadesGame()
game.run()
