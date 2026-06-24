import board
import deckclass


def betting_round(pokerGame, players, starting_index, current_bet):
        active_players = [p for p in players if p.active]
        if len(active_players) <=1:
            pokerGame.collect_bets(players)
            return
        
        current_index = starting_index
        while not pokerGame.is_round_over(players, current_bet):
            player = players[current_index]

            if not player.active:
                current_index = pokerGame.get_next_active(players, current_index)
                continue

            if player.stack == 0:
                player.has_acted = True
                current_index= pokerGame.get_next_active(players, current_index)
                continue

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


            current_index = pokerGame.get_next_active(players, current_index)
        
        pokerGame.collect_bets(players)

def get_villain_action(player, current_bet):
    """
    To Do implement this
    """
    call_amount = current_bet - player.current_bet
    if call_amount == 0:
        player.has_acted = True
        print(f"{ player.position.value} checks.")
        return 'check', 0
    else:
        amount = min(call_amount, player.stack)
        player.stack -= amount
        player.current_bet += amount
        player.has_acted = True
        print(f" {player.position.value} calls {amount}")
        return 'call', amount

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
           