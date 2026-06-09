import random
import board
from enum import Enum

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Position(Enum):
    SB = "sb"
    BB = "bb"
    UTG = "utg"
    MP = "mp"
    CO = "co"
    BTN = "btn"

class Players():
    def __init__(self, startingStack = 100):
        self.type=''
        self.hand = []
        self.stack = startingStack
        self.position = ''
        self.active = True
        self.current_bet = 0
        self.has_acted = False
    def __repr__(self):
        return f'{self.position} is {self.type} -> {self.hand}'

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
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

class Card:
    def __init__(self,suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.suit.name.title()} of {self.rank.name.title()}"

    def __repr__(self):
        return f'({self.rank.value}, {self.suit.value})'

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

    def dealFlop(self):
        self.cards.pop()
        return [self.cards.pop() for _ in range(3)]

    def dealTurnRiv(self):
        self.cards.pop()
        return(self.cards.pop())

    def __len__(self):
        return len(self.cards)



class PokerGame:
    def __init__(self,numOfPlayer = 1, startingStack = 100, bigBlind = 2):
        self.deck = Deck()
        self.deck.shuffle()
        self.button_index = 0
        self.numOfPlayer = numOfPlayer
        self.startingStack = startingStack
        self.bigBlind = bigBlind
        self.smallBlind = bigBlind // 2
        self.current_street_bet = 0
        self.pot = 0

    def getPosition(self,num_players):
        if num_players < 2 or num_players > 6:
            raise ValueError("Number of Player must be between 2 and 6")
        
        all_positions = [
            Position.BTN,
            Position.SB,
            Position.BB,
            Position.UTG,
            Position.MP,
            Position.CO
        ]

        return all_positions[:num_players]

    def dealTable(self, numPlayer):
        hero_index = random.randint(0, numPlayer -1)
        positions = self.getPosition(numPlayer)
        seatedTable = [Players() for _ in range(numPlayer)]
        
        for i in range(numPlayer):
            #need to add so that if there are not enough players
            seatedTable[i].position = positions[i]

        for i, player in enumerate(seatedTable):
            if i == hero_index:
                player.type = "HERO"
            else:
                player.type = "VILLAIN"
        

        sb_index = next(i for i, p in enumerate(seatedTable) if p.position== Position.SB)
        dealing_order = seatedTable[sb_index:] + seatedTable[:sb_index];

        for i in range(2):
            for player in dealing_order:
                player.hand.append(self.deck.deal(1)[0])
        return seatedTable
    

    # need to deal one hand to each player one by one.
    # write it as loop dealing a single hand to each of the players.
    # make it so that there is a max number of players that can play.
    def dealHand(self):
        return self.dealTable(self.numOfPlayer)

    def flop(self):
        return self.deck.dealFlop()
    def turnRiv(self):
        return self.deck.dealTurnRiv()
    
    def get_next_active(self, players, current_index):
        n = len(players)
        for i in range(1, n + 1):
            next_index = (current_index + i) % n
            if players[next_index].active:
                return next_index
        return None

    def is_round_over(self,players, current_bet):
        for player in players:
            if player.active:
                if not player.has_acted or player.current_bet != current_bet:
                    return False

        return True

    def betting_round(self, players, starting_index, current_bet):
        current_index = starting_index
        while not self.is_round_over(players, current_bet):
            player = players[current_index]
            if player.type == 'HERO':
                action, amount = get_hero_action(player, current_bet)
            else:
                action, amount = get_villain_action(player, current_bet)
            
            if(action == 'fold'):
                player.active = False
                player.has_acted = True
            if(action == "call"):
                player.active = True
                player.has_acted = True
                player.stack = player.stack - current_bet + player.current_bet
                player.current_bet = current_bet
            if(action == "raise"):
                if(amount < 2 * current_bet):
                    print("Unvalid amount to raise")
                else:
                    player.current_bet = amount
                    player.stack = player.stack - (amount - player.current_bet)
                    player.has_acted = True
                    current_bet = amount
                    for activePlayer in players:
                        if activePlayer != player and activePlayer.active == True:
                            activePlayer.has_acted = False


            current_index = self.get_next_active(players, current_index)
        
        self.collect_bets(players)

    def collect_bets(self, players):
        for player in players:
            self.pot += player.current_bet
            player.current_bet = 0
            player.has_acted = False



