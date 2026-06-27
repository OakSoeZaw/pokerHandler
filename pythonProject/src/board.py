import deckclass
import evaluator
import betting
from gto import GTO, lookup

from hand_parser import normalize_hand

activePlayer = []
openAction = True
showdown = False
TableSeat = []


def gameStart(pokerGame):
    players = pokerGame.dealHand()

    agressor = None
    hero = None
    num_raises = 0
    normalized_hands = {}

    for i, player in enumerate(players):
        print(player)

        card1, card2 = player.hand[0], player.hand[1]
        normalized_hand = normalize_hand(card1, card2)
        normalized_hands[player] = normalized_hand

    # preFlop actions
    starting_idx = pokerGame.post_blinds(players)
    print(f"\n-- Preflop | Pot: {pokerGame.pot} ---")
    hero, hero_actions = betting.betting_round(
        pokerGame, players, starting_idx, pokerGame.bigBlind
    )

    print(f"----Validating Actions ---")
    for item in hero_actions:
        situation = item["situation"]
        raiser = item["raiser_position"]
        raiser_position = raiser if raiser else None
        correct_action = lookup(
            hero.position.value, situation, normalized_hands[hero], raiser_position
        )

        check_result = check_action(correct_action, item["action"])
        if check_result:
            print("Right Decision")
        else:
            print(f"Wrong! GTO says {correct_action}")


def check_action(correct_action, actual_action):
    if correct_action == "raise_bluff" and actual_action in ("raise", "fold"):
        return True
    elif correct_action == "raise_value" and actual_action == "raise":
        return True
    elif correct_action == actual_action:
        return True
    else:
        return False


if __name__ == "__main__":
    pokerGame = deckclass.PokerGame(numOfPlayer=6)  # max player is 6

    gameStart(pokerGame)
