import random

from card import Card
from behaviour import *
from thinking import Thinking
from action import *


class Player:
    """
    Everything that the player manages is in this class
    That includes the players believes, knowledge the player has and its values
    The player also manages its own side of the board
    """

    def __init__(self, name, behaviour: Behaviour):
        self.name = name
        self.behaviour = behaviour
        self.skips = 0
        self.hassle = []
        self.stash = []
        self.hand = []
        self.knowledge_base = Thinking(self)
        self.score = 0

    def eval_self(self) -> dict:
        """ adds up card values over the stash and hand of a player, regardless of the banker """
        # evaluate stash
        protected = 0
        stash = 0
        for c in self.stash:
            if c.type == "pd":
                stash += c.value
            elif c.type == "pr":
                protected += c.value

        # evaluate hand
        hand = 0
        for card in self.hand:
            if card.type == "pd" or card.type[0] == 'd':
                hand -= card.value

        return {"protected": protected, "stash": stash, "hand": hand}

    def take_hand_card(self, ctype: str, cvalue: int = 0) -> Card:
        """ take one card from hand, removes it """
        for i, c in enumerate(self.hand):
            if c.type == ctype:
                if cvalue:
                    if c.value == cvalue:
                        return self.hand.pop(i)
                else:
                    return self.hand.pop(i)

    def check_hand_card(self, ctype, cvalue: int = 0) -> Card:
        """ check, if hand contains card of specified type """
        for c in self.hand:
            if c.type == ctype:
                if cvalue:
                    if c.value == cvalue:
                        return c
                else:
                    return c

    def highest_stashed_peddle_value(self) -> int:
        """ return highest peddle value, else return 0"""
        highest = 0
        peddles = [pd.value for pd in self.stash if pd.type == "pd"]
        if peddles:
            highest = max(peddles)
        return highest

    def lowest_stashed_peddle_value(self) -> int:
        """ return lowest peddle value, else return 0"""
        lowest = 0
        peddles = [pd.value for pd in self.stash if pd.type == "pd"]
        if peddles:
            lowest = min(peddles)
        return lowest

    def take_lowest_stash_card(self) -> Card:
        """ take lowest peddle from stash, removes it """
        lowest = 200000
        lowest_idx = -1
        for i, c in enumerate(self.stash):
            if c.type == "pd" and c.value < lowest:
                lowest_idx = i
                lowest = c.value
        if lowest_idx >= 0:
            return self.stash.pop(lowest_idx)

    def take_highest_stash_card(self) -> Card:
        """ take highest peddle from stash, removes it """
        highest = 0
        highest_idx = -1
        for i, c in enumerate(self.stash):
            if c.type == "pd" and c.value > highest:
                highest_idx = i
                highest = c.value
        if highest_idx >= 0:
            return self.stash.pop(highest_idx)

    def take_stash_card(self, value) -> Card:
        """ take specific stashed peddle card with defined value """
        for i, c in enumerate(self.stash):
            if c.type == "pd" and c.value == value:
                return self.stash.pop(i)

    def check_stash_card(self, ctype: str, value=0) -> Card:
        """ check, if stash contains card of specified type """
        for c in self.stash:
            if c.type == ctype:
                if value:
                    if c.value == value:
                        return c
                else:
                    return c

    def check_stash_for_protection(self, value) -> list[int]:
        """
        check stash for combination of peddle cards for protection, then return their indexes
        always try to find as little amount of cards to be protected as possible
        """
        peddle = []
        for i, c in enumerate(self.stash):
            if c.type == "pd":
                peddle.append((i, c))
        sorted_peddle = sorted(peddle, key=lambda el: el[1].value, reverse=True)
        collected_peddle = []
        found_combination = False
        for c in sorted_peddle:
            if c[1].value > value:
                continue
            else:
                collected_peddle.append(c)
                if sum(el[1].value for el in collected_peddle) == value:
                    found_combination = True
                    break
        if found_combination:
            return [el[0] for el in collected_peddle]

    def heated(self) -> int:
        """ check how the market is heated, returns type of heat """
        if self.hassle and self.hassle[-1].type == "hn":
            return self.hassle[-1].value

    # what would the player do when it is their turn
    def move(self, game: Grass):
        """
        This function takes all the steps a player would take to make a move
        First the player skips or draw a card if possible (else the game ends)
        Then the player evaluates their position and interacts with the game
        The player will evaluate all options for interactions and choose to
        offer or accept open trades with other players
        After trading phase, the player plays a card
        :return: if the game hasn't ended after the move, it returns True
        """
        game.turn += 1
        # check if we need to skip a round
        if self.skips:
            game.handle_action(Skip(self))
            return True

        # TODO employ policy to evaluate and find good actions
        # evaluate cards and needs
        evaluation = self.eval_self()

        # if cards are left in the deck draw, else the game ends by the rules
        # TODO implement drawing from discard pile
        if game.deck:
            game.handle_action(DrawCard(self, "deck"))
        else:
            return False

        # TODO implement trading (in progress)
        self.trade()

        # play a card
        # TODO play best evaluated card
        c = random.choice(self.hand)
        while c.type in ["ba", "mc"]:
            c = random.choice(self.hand)
            if c.type == "mc" and c.playable(self):
                break

        if c.type in ["mc", "mo", "pd", "hf", "st", "eu", "ds", "dc", "du", "pr"]:
            game.handle_action(PlayCard(self, c.type, [self, game]))
        elif c.type == "hn":
            rand_player = random.choice(game.players)
            while rand_player is self:
                rand_player = random.choice(game.players)
            game.handle_action(PlayCard(self, c.type, [game, rand_player]))
        elif c.type == "pf":
            game.handle_action(PlayCard(self, c.type, [self, game, self.lowest_stashed_peddle_value()]))
        elif c.type == "sn":
            rand_player = random.choice(game.players)
            while rand_player is self:
                rand_player = random.choice(game.players)
            game.handle_action(PlayCard(self, c.type, [self, game, rand_player, rand_player.highest_stashed_peddle_value()]))
        return True

    # offer or accept trades
    def trade(self):
        """ everything that has to do with the player trading """
        # TODO employ policy and evaluation of trade possibilities and needs
        # TODO let all players have a shot at trading while it is trading phase
        # but make sure it doesn't take too long!
        pass

    def trade_offer(self, offer=None):
        """
        Offer or accept trades: If an offer is given, the offer is evaluated
        If the evaluation is positive, the offer is either agreed on or accepted
        else the offer is rejected and there could even be counter offers
        If the offer doesn't target the player, it might react with a counter offer as well
        """
        # TODO implement card trading options
        return False

    # send a card to the player left of you before knowing the card receiving, popping that card from the hand
    def send_card_left(self):
        # send any negative cards left, else the one with the minimum value
        # TODO choose good card left when paranoia cards are played based on policy
        c = random.choice(self.hand)
        return False
