import random
import enum as Enum

class Suit(Enum):
    HEARTS = 'h'
    DIAMONDS = 'd'
    CLUBS= 'c'
    SPADES = 's'

class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Card:
    def __init__(self,suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.suit.name.title()} of {self.rank.name.title()}"

    def __repr__(self):
        return f'Card({self.suit}, {self.rank})'

    def __eq__(self,other):
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return hash((self.suit,self.rank))

class Deck:
    def __init__(self):
        self.cards = [Card(suit,rank) for suit in Suit for rank in Rank]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self,numCard = 1):
        if numCard > len(self.cards):
            raise ValueError("There is no enough card to deal")
        return [self.cards.pop() for _ in range(numCard)]

    def __str__(self):
        return f'Deck with {len(self.cards)} remaining'

    def __len__(self):
        return len(self.cards)


