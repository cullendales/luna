from text_and_audio.tts import respond
from text_and_audio.stt import get_command
from random import choice
#can check logs to determine how much money player has
# can ask them to place best

affirmation = {
    'yes',
    'yeah',
    'hit',
    'me',
}

suits = [
    'hearts',
    'diamonds',
    'spades',
    'clubs',
]

card_values = {
    'Ace': 1, #can also be 11
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'jack': 10,
    'queen': 10,
    'king': 10
}

def get_player_cards(player_cards):
    respond("Your cards are ")
    for card in player_cards:
        respond(f"{card}")


def deal(dealt_cards):
    card_num = choice(card_values)
    card = card_num.key + "of" + choice(suits)
    while card in dealt_cards:
        card_num = choice(card_values)
        card = card_num.key + "of" + choice(suits)
    return card, card_num


def play_blackjack(cheetah):
    dealt_cards = []
    player_cards = {}
    dealer_cards = {}
    player_hand_total = dealer_hand_total = 0

    for i in range(4):
        card, card_value = deal(dealt_cards)
        dealt_cards.append(card)
        if i % 2 == 0:
            player_cards.add(card)
            player_hand_total += card_value
        else:
            dealer_cards.add(card)
            dealer_hand_total += card_value
        
    get_player_cards(player_cards)
    
    while player_hand_total <= 21:
        respond("Do you want to hit?")
        want_hit = get_answer(cheetah)
        if next(affirmation in want_hit):
            card, card_value = deal(dealt_cards)
            dealt_cards.append(card)
            player_hand_total += card_value
        else:
            break
    
    if player_hand_total > 21:
        respond("Bust! Dealer wins")
    
    else:
        while player_hand_total > dealer_hand_total:
            card, card_value = deal(dealt_cards)
            dealt_cards.append(card)
            dealer_hand_total += card_value
    
    if dealer_hand_total > 21:
        respond("Dealer Busted. You win!")

    

    
    


