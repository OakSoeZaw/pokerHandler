import deckclass

heroCall = False
villainCall = False
showdown = False
TableSeat= []

'''Problem with the input. It runs best with 6 players as every position got
declared. It doesn't work when there is less player and user input
the position that was not added to the players.'''


def gameStart(pokerGame):
    pokerTable = pokerGame.dealHand()
    for hand in pokerTable:
        if hand.type == "HERO":
            print(hand)


    # need to add a datastructure that will store the flop and the final 
    # board
    flop = pokerGame.deck.dealFlop()
    print(flop)



if __name__ == '__main__':
    pokerGame = deckclass.PokerGame(numOfPlayer=3) # max player is 6

    gameStart(pokerGame)



