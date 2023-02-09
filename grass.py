import random
from card import *
from action import *
from player import Player
### Grass Rules:
# 24 different card types
# - pebble money cards (4): 12x5k, 10x25k, 5x50k, 1x100k
# - heat on (4) and heatoff (5): 12x heaton, 20x heatoff, 4x pay fine
# - nirvana cards (6): 5x stonehigh, 1x euphoria
# - paranoia cards (8): 4x sold out, 3x Doublecrossed, 1 utterly wiped out
# - protection cards (6): 2x 50k, 4x 25k
# - skim cards (5): 4x steal, 1x banker
# - market cards ( 15): 10x open market, 5x close market

### Players play in turns and can trade cards 1 for 1 when its their turn
# - need open market to start shashing peddle
# - market can be heated and heat can be removed with coutner heat off ard or for lowest money amount and pay fine
# - market needs to be free of heat to close market, as well as 50k needs to be stashed
# - market closes for everyone
# - paranoia cards let every player send one card to the left
# -
# - first to be at 250k total wins


class Grass:
    def __init__(self, players: list[Player]):
        self.status = "initializing"
        self.players = players
        self.waste = []
        self.waste_status = "discarded"
        self.deck = []
        self.card_pool = []
        self.rounds = []
        self.turn = 0
        self.winner = "none"

    def discard(self, card: Card):
        """ handles discarding a card to the discard pile """
        self.waste_status = "discarded"
        self.waste.append(card)

    def burn(self, card: Card):
        """ handles playing a card to the discard pile """
        self.waste_status = "played"
        self.waste.append(card)

    def initialize_round(self):
        for pl in self.players:
            pl.hand = []
        self.waste = []
        self.deck = []
        decks = len(self.players)//10 + 1
        for i in range(decks):
            self.deck.extend(new_deck())
        random.shuffle(self.deck)

    def find_banker(self):
        for i, pl in enumerate(self.players):
            if pl.check_hand_card("ba"):
                return i
        return -1

    # counting up the stashes and subtracting/adding losses from hands and the banker
    def score_round(self):
        banker = self.find_banker()
        round_summary = []
        for pl in self.players:
            values = pl.eval_self()
            stash = getattr(values, "stash")
            if banker >= 0:
                self.players[banker].score += 0.2 * stash
                stash -= 0.2 * stash
            round_result = stash + getattr(values, "protected") + getattr(values, "hand")
            pl.score += round_result
            round_summary.append(round_result)
        return round_summary

    def handle_action(self, action: Action):
        self.rounds[-1].append(action)
        action.effect(self)


    def play_round(self):
        self.status = "setup"
        self.rounds.append([])
        self.turn = 0
        self.initialize_round()
        self.card_pool = self.deck.copy()

        # draw initial hand cards
        for count in range(6):
            for pl in self.players:
                pl.hand.append(self.deck.pop())

        # initial card on waste pile
        self.waste.append(self.deck.pop())

        # game mainloop
        self.status = "playing"

        #starting player
        turn_player = len(self.rounds) % len(self.players)
        while self.status == "playing":
            pl = self.players[turn_player]
            if not(pl.move()):
                self.status = "cards ran out"
            turn_player = (turn_player + 1) % len(self.players)

        self.score_round()
        self.status = "between rounds"
