import board
import math
from treys import Evaluator, Card as treysCard
from deckclass import Suit, Rank, Players

suitChange = {
    Suit.HEARTS : 'h',
    Suit.DIAMONDS : 'd',
    Suit.CLUBS : 'c',
    Suit.SPADES : 's'
}

def evaluateHand(board, players) -> dict:
    playerScores = {} #player : (int) playerScore
    treysPlayers = []
    evaluator = Evaluator()
    treyBoard = handToTreys(board)
    
    for i,player in enumerate(players):
        if player.active == True:
            treyHand = handToTreys(player.hand)
            treysPlayers.append(treyHand)
            playerScores[player] = evaluator.evaluate(treyBoard, treyHand)

    return playerScores

def findWinner(playersScores) -> Players:
    """
    input is a dict or player to scores
    and return a Player
    """
    if not playersScores:
        return None

    winner = None
    bestScore = math.inf
    for player, score in playersScores.items():
        if score < bestScore:
            bestScore = score
            winner = player
    
    return winner
        


# def switchToTreysCard(players):
#     for player in players:
#         if(player.Suit )

def handToTreys(hand):
    """
    Return an hand array that is converted to 
    Treys requirement
    """
    treyHand = []
    for card in hand:
        rank = card.rank.value
        suit = suitChange[card.suit]
        treyHand.append(treysCard.new(rank + suit))
    return treyHand