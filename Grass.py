import random
import Card
import Player

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


def new_deck():
    deck = []

    # market open and closed cards
    deck.extend([Card.MarketOpen() for i in range(10)])
    deck.extend([Card.MarketClose() for i in range(5)])

    # peddle cards
    deck.extend([card("pd", 5000) for i in range(12)])
    deck.extend([card("pd", 25000) for i in range(10)])
    deck.extend([card("pd", 50000) for i in range(5)])
    deck.append(card("pd", 100000))

    # heat on and off cards and pay fine, matching value = same heat
    deck.extend([card("hn", 1) for i in range(3)])
    deck.extend([card("hn", 2) for i in range(3)])
    deck.extend([card("hn", 3) for i in range(3)])
    deck.extend([card("hn", 4) for i in range(3)])
    deck.extend([card("hf", 1) for i in range(5)])
    deck.extend([card("hf", 2) for i in range(5)])
    deck.extend([card("hf", 3) for i in range(5)])
    deck.extend([card("hf", 4) for i in range(5)])
    deck.extend([card("hp", 0) for i in range(4)])

    # nirvana cards stonehigh and euphoria
    deck.extend([card("ns", 1) for i in range(5)])
    deck.append(card("ne", 1))

    # paranoia cards
    deck.extend([card("ds", 25000) for i in range(4)])
    deck.extend([card("dc", 50000) for i in range(3)])
    deck.extend([card("du", 100000) for i in range(1)])

    # protection cards
    deck.extend([card("pr", 25000) for i in range(4)])
    deck.extend([card("pr", 50000) for i in range(2)])

    # skim cards
    deck.extend([card("sn", 0) for i in range(4)])
    deck.append(card("ba", 0))

    return deck


standard_eval = {
    "hand": {
        "mo": 7500,
        "mc": 55000,
        "ps": 4000,
        "pl": 15000,
        "pb": 30000,
        "ph": 15000,
        "hn": 3000,
        "hf": 45000,
        "hp": 0,
        "ns": 60000,
        "ne": 120000,
        "ds": -15000,
        "dc": -40000,
        "du": -100000,
        "al": 25000,
        "ab": 50000,
        "sn": 60000,
        "ba": 100000
    },
    "stash": {
        "mo": 0,
        "ps": 4000,
        "pl": 20000,
        "pb": 40000,
        "ph": 100000,
        "hn": 0,
        "al": 25000,
        "ab": 50000,
    },
    "status": {
        "ready": 0,
        "mo": 20000,
        "heated": -50000,
        "skip": -35000,
    }
}


class grass:
    def __init__(self, players):
        self.players = players
        self.waste = []
        self.deck = []
        self.round = 0
        self.winner = "none"

    def initialize_round(self):
        for pl in self.players():
            pl.hand = []
        self.waste = []
        self.deck = []
        decks = len(self.players)//10 + 1
        for i in range(decks):
            self.deck.extend(new_deck())
        random.shuffle(self.deck)

    # counting up the stashes and subtracting/adding losses from hands and the banker
    def score_round(self):
        banker = True in [pl.banker for pl in self.players]
        for pl in self.players:
            values = pl.eval_self()
            stash = getattr(values, "stash")
            if banker:
                banker.score += 0.2 * stash
                stash *= 0.8
            pl.score += stash + getattr(values, "protected") + getattr(values, "hand")

    def play_round(self):
        self.round += 1
        self.initialize_round()
        card_pool = self.deck.copy()

        # draw initial hand cards
        for count in range(6):
            for pl in self.players:
                pl.hand.append(self.deck.pop())

        # initial card on waste pile
        self.waste.append(self.deck.pop())

        # game mainloop
        moves = True

        #starting player
        turn_player = self.round % len(self.players)
        while moves:
            pl = self.players()[turn_player]
            moves = pl.move(self)
            turn_player = (turn_player + 1) % len(self.players)

