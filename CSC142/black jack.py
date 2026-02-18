import random

# draw a random card from the deck
def draw_card(deck):
    card = random.choice(deck)
    deck.remove(card)
    return card


# calculate the total score of a hand
def calculate_score(hand):
    total = 0
    aces = 0

    for card in hand:
        if card == "J" or card == "Q" or card == "K":
            total += 10
        elif card == "A":
            aces += 1
            total += 11
        else:
            total += int(card)

    # fix ace value if score is too high
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


# print current game status
def print_status(player_hand, dealer_hand, show_dealer_card=True):
    if show_dealer_card:
        print("Dealer card:", dealer_hand[0])
    else:
        print("Dealer hand:", dealer_hand)

    print("Your hand:", player_hand)
    print("Your score:", calculate_score(player_hand))
    print()


def main():
    deck = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    random.shuffle(deck)

    dealer_hand = []
    player_hand = []

    # dealer draws first card
    dealer_hand.append(draw_card(deck))

    # player draws two cards
    player_hand.append(draw_card(deck))
    player_hand.append(draw_card(deck))

    print("Welcome to Simple Blackjack!")
    print_status(player_hand, dealer_hand)

    # player turn
    while True:
        choice = input("Hit or stay? ").lower()

        if choice == "hit":
            player_hand.append(draw_card(deck))
            print_status(player_hand, dealer_hand)

            if calculate_score(player_hand) > 21:
                print("You busted! Dealer wins.")
                return

        elif choice == "stay":
            break
        else:
            print("Invalid input, please type hit or stay.")

    # dealer turn
    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(draw_card(deck))

    dealer_score = calculate_score(dealer_hand)
    player_score = calculate_score(player_hand)

    print("\nFinal Results:")
    print("Dealer hand:", dealer_hand)
    print("Dealer score:", dealer_score)
    print("Your hand:", player_hand)
    print("Your score:", player_score)

    if dealer_score > 21:
        print("Dealer busted! You win!")
    elif dealer_score > player_score:
        print("Dealer wins.")
    elif dealer_score < player_score:
        print("You win!")
    else:
        print("It's a tie!")


main()
