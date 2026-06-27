import random
import deckclass
from gto import GTO, lookup
from hand_parser import normalize_hand


def betting_round(pokerGame, players, starting_index, current_bet) -> deckclass.Players:
    raiser = None
    hero = None
    first_raiser= None
    hero_actions = []
    hero_was_last_raiser = False
    num_raises = 0
    active_players = [p for p in players if p.active]
    if len(active_players) <= 1:
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
            current_index = pokerGame.get_next_active(players, current_index)
            continue

        if player.type == "HERO":
            hero = player
            action, amount = get_hero_action(player, current_bet, num_raises, raiser, hero_was_last_raiser)
            situation = get_situation(num_raises, first_raiser, player, hero_was_last_raiser)
            hero_actions.append(
                {
                    "action": action,
                    "situation": situation,
                    "raiser_position": raiser.position.value if raiser else None,
                }
            )
        else:
            action, amount = get_villain_action(player, current_bet, num_raises, first_raiser, hero_was_last_raiser)

        if action == "fold":
            player.active = False
            player.has_acted = True
        if action == "call":
            player.active = True
            player.has_acted = True
            player.stack = player.stack - current_bet + player.current_bet
            player.current_bet = current_bet
        if action == "raise":
            if amount < 2 * current_bet:
                print("Unvalid amount to raise")
            else:
                if num_raises == 0: 
                    first_raiser = player
                if player.type == "HERO":
                    hero_was_last_raiser = True
                else:
                    hero_was_last_raiser = False
                raiser = player
                num_raises += 1
                player.stack = player.stack - (amount - player.current_bet)
                player.current_bet = amount
                player.has_acted = True
                current_bet = amount
                for activePlayer in players:
                    if activePlayer != player and activePlayer.active == True:
                        activePlayer.has_acted = False

        current_index = pokerGame.get_next_active(players, current_index)

    pokerGame.collect_bets(players)
    return hero, hero_actions


def get_villain_action(player, current_bet, num_raises, raiser, hero_was_last_raiser):
    """
    Look up hand value in GTO and respond
    """
    situation = get_situation(num_raises, raiser, player, hero_was_last_raiser)

    card1, card2 = player.hand[0], player.hand[1]
    normalized_hand = normalize_hand(card1, card2)
    raiser_position = raiser.position.value if raiser else None
    action = lookup(player.position.value, situation, normalized_hand, raiser_position)

    if action == "call":
        call_amount = current_bet - player.current_bet
        if call_amount == 0:
            player.has_acted = True
            print(f"{ player.position.value} checks.")
            return "check", 0
        else:
            amount = min(call_amount, player.stack)
            player.stack -= amount
            player.current_bet += amount
            player.has_acted = True
            print(f" {player.position.value} calls {amount}")
            return "call", amount
    elif action == "raise_value":
        amount = min(current_bet * 3, player.stack)
        print(f" {player.position.value} raise {amount}")
        return "raise", amount
    elif action == "raise_bluff":
        if random.random() < 0.20:
            amount = min(current_bet * 3, player.stack)
            print(f" {player.position.value} raise {amount}")
            return "raise", amount
        else:
            print(f" {player.position.value} fold")
            return "fold", 0
    elif action == "fold":
        print(f" {player.position.value} fold")
        return "fold", 0


def get_hero_action(player, current_bet, num_raises, raiser, hero_was_last_raiser):
    call_amount = current_bet - player.current_bet
    print(
        f"\nYour hand: {player.hand} | Stack: {player.stack} | To call: {call_amount}"
    )

    options = []
    if call_amount == 0:
        options = ["check (c)", "bet (b)", "fold (f)"]
    else:
        options = ["call (c)", "raise (r)", "fold (f)"]

    print(f"Options: {' / '.join(options)}")

    while True:
        choice = input("Action: ").strip().lower()

        if choice == "f":
            player.active = False
            player.has_acted = True
            return "fold", 0

        elif choice == "c":
            amount = min(call_amount, player.stack)
            player.stack -= amount
            player.current_bet += amount
            player.has_acted = True
            return "call", amount

        elif choice in ("b", "r"):
            min_raise = current_bet + deckclass.PokerGame(bigBlind=2).bigBlind
            try:
                amount = int(input(f" Amount (min {min_raise}) :  "))
                if amount < min_raise:
                    print(" At least twice the blinds")
                    continue
                bet_increase = amount - player.current_bet
                if bet_increase > player.stack:
                    print("Not enough chips")
                    continue
                player.stack -= bet_increase
                player.current_bet = amount
                player.has_acted = True

                return "raise", amount
            except ValueError:
                print("Enter a number. ")
        else:
            print("Invalid input")


def get_situation(
    num_raises: int, first_raiser: deckclass.Players, currentPlayer: deckclass.Players, hero_was_last_raiser : bool
):
    if num_raises == 0:
        return "rfi"
    elif num_raises == 1:
        return "facingRfi"
    elif num_raises > 1 and currentPlayer.type == "HERO" and hero_was_last_raiser:
        return "rfi_vs_3bet"
    elif num_raises > 1 and currentPlayer.type == "VILLAIN" and first_raiser == currentPlayer:
        return "rfi_vs_3bet"
    else:
        return "facingRfi"
