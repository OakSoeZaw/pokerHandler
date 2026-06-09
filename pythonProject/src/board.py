import deckclass

activePlayer = []
openAction = True
showdown = False
TableSeat= []


def get_hero_action(player, current_bet):
    call_amount = current_bet - player.current_bet
    print(f"\nYour hand: {player.hand} | Stack: {player.stack} | To call: {call_amount}")

    options = []
    if call_amount == 0:
        options = ["check (c)", "bet (b)", "fold (f)"]
    else:
        options = ["call (c)", "raise (r)", "fold (f)"]

    print(f"Options: {' / '.join(options)}")

    while True:
        choice = input("Action: ").strip().lower()

        if choice == 'f':
            player.active = False
            player.has_acted = True
            return 'fold', 0
        
        elif choice == 'c':
            amount = min(call_amount, player.stack)
            player.stack -= amount
            player.current_bet += amount
            player.has_acted = True
            return 'call', amount
        
        elif choice in ('b', 'r'):
            min_raise = current_bet + deckclass.PokerGame(bigBlind=2).bigBlind
            try:
                amount = int(input(f" Amount (min {min_raise}) :  "))
                if amount < min_raise:
                    print( " At least twice the blinds")
                    continue
                bet_increase = amount - player.current_bet
                if bet_increase > player.stack:
                    print("Not enough chips")
                    continue
                player.stack -= bet_increase
                player.current_bet = amount
                player.has_acted = True
                
                return 'raise', amount
            except ValueError:
                print("Enter a number. ")
        else:
            print("Invalid input")
        
def get_villain_action(player, current_bet):
    """
    To Do implement this
    """
    call_amount = current_bet - player.current_bet
    if call_amount == 0:
        player.has_acted = True
        print(f"{ player.postition.value} checks.")
        return 'check', 0
    else:
        amount = min(call_amount, player.stack)
        player.stack -= amount
        player.current_bet += amount
        player.has_acted = True
        print(f" {player.position.value} calls {amount}")
        return 'call', amount




def gameStart(pokerGame):
    players = pokerGame.dealHand()
    for hand in players:
        print(hand)
    # while(openAction):


    #preFlop actions
    starting_idx = pokerGame.post_blinds(players)
    print(f"\n-- Preflop | Pot: {pokerGame.pot} ---")

    

    


if __name__ == '__main__':
    pokerGame = deckclass.PokerGame(numOfPlayer=3) # max player is 6

    gameStart(pokerGame)



