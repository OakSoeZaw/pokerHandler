from deckclass import Card

RANK_ORDER = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

def normalize_hand(card1: Card, card2: Card) -> str:
    r1 = card1.rank.value
    r2 = card2.rank.value

    if RANK_ORDER.index(r1) < RANK_ORDER.index(r2):
        r1, r2 = r2, r1
        card1, card2 = card2, card1
    
    if r1 == r2:
        return f"{r1}{r2}"
    
    suited = card1.suit == card2.suit
    suffix = 's' if suited else 'o'
    return f"{r1}{r2}{suffix}"
