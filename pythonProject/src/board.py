import deckclass
import evaluator
import betting

activePlayer = []
openAction = True
showdown = False
TableSeat= []





def gameStart(pokerGame):
    players = pokerGame.dealHand()

    for i,hand in enumerate(players):
        print(hand)

    #preFlop actions
    starting_idx = pokerGame.post_blinds(players)
    print(f"\n-- Preflop | Pot: {pokerGame.pot} ---")
    betting.betting_round(pokerGame,players, starting_idx, pokerGame.bigBlind)

    #flop
    board = pokerGame.flop()
    print(f"\n-- Board(Flop): {board} | Pot: {pokerGame.pot} ---")
    betting.betting_round(pokerGame,players, 1,current_bet = 0)
    resultFlop = evaluator.evaluateHand(board, players)

    #turn
    turn = pokerGame.turnRiv()
    board.append(turn)
    print(f"\n -- Board(Turn): {board} | Pot: {pokerGame.pot} ---")
    betting.betting_round(pokerGame,players, 1, current_bet = 0)
    resultTurn = evaluator.evaluateHand(board, players)

    #River
    river = pokerGame.turnRiv()
    board.append(river)
    print(f"\n -- Board(River): {board} | Pot: {pokerGame.pot} --")
    betting.betting_round(pokerGame,players, 1, current_bet = 0)
    resultRiver = evaluator.evaluateHand(board, players)

    print(f"\n--- Showdown | Final pot: {pokerGame.pot}---")

    print("---Flop ---")
    for item in resultFlop:
        print(item)
    
    print("--Turn--")
    for item in resultTurn:
        print(item)
    
    print("--River--")
    for item in resultRiver:
        print(item)

    winner = evaluator.findWinner(resultRiver)
    print(winner)
    
    


if __name__ == '__main__':
    pokerGame = deckclass.PokerGame(numOfPlayer=3) # max player is 6

    gameStart(pokerGame)



