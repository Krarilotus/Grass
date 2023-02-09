import Grass
import Card


class Player:
    """
    Everything that
    """
    def __init__(self, name, behaviour: str, card_eval: dict, game: Grass):
        self.name = name
        self.behaviour = behaviour
        self.card_eval = card_eval
        self.skips = 0
        self.hassle = []
        self.stash = []
        self.hand = []
        self.knowledge_base = {}
        self.score = 0
        self.banker = False
        self.game = game

    def eval_self(self) -> dict:
        """ simply adds up card values over the stash and hand of a player, regardless of the banker """
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

    def take_hand_card(self, ctype) -> Card:
        """ take one card from hand, removes it """
        for i, c in enumerate(self.hand):
            if c.type == ctype:
                return self.hand.pop(i)

    def check_hand_card(self, ctype) -> Card:
        """ check hand for specific card, if found return the card """
        for c in self.hand:
            if c.type == ctype:
                return c

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

    def check_stash_card(self, ctype) -> Card:
        """ check stash for specific card, if found return card """
        for c in self.stash:
            if c.type == ctype:
                return c

    def check_stash_for_protection(self, value) -> list[int]:
        """
        check stash for combination of peddle cards for protection, then return their indexes
        always try to find as little amount of cards to be protected as possible
        """
        peddle = []
        for i, c in enumerate(self.stash):
            if c.type == "pd":
                peddle.append((i,c))
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

    # deals the card effects if possible, then returns True.
    # If a card can't be played normally, it will return false
    def playable(self, c: Card, target, play=False):
        """
        :param c: card to be checked/played
        :param play: playing the card of question as well
        :return:
        """
        # market opened
        chosen_card = self.take_hand_card(c)
        if c.type == "mo":
            if "mo" in [sc.type for sc in self.stash]:
                if play:
                    self.game.waste.append(chosen_card)
                return False
            else:
                if play:
                    self.stash.append(chosen_card)
                return True

        # market closed
        elif c.type == "mc":
            marketcap = getattr(self.eval_self(), "stash") + getattr(self.eval_self(), "protected")
            if self.heated() or marketcap < 50000:
                if play:
                    self.game.waste.append(chosen_card)
                return False
            else:
                if play:
                    self.game.score_round()
                return True

        # peddle cards
        elif c.type == "pd":
            if self.heated() or not self.check_stash_card("mo"):
                if play:
                    self.game.waste.append(chosen_card)
                return False
            else:
                if play:
                    self.game.stash.append(chosen_card)
                return True

        #




        return True

    # what would the player do when it is their turn
    def move(self):
        # check if we need to skip a round
        if self.status:
            self.status -= 1
            return True

        # if cards are left draw
        # TODO implement drawing from discard pile
        if self.game.deck:
            self.hand.append(self.game.deck.pop())

        # As long as holding cards, the player can do sth
        if not self.hand:
            return False

        # employ the players policy to pick the cards to play
        if self.behaviour == "simple":
            evaluation = self.eval_self()

            # always try to close the market asap
            type = "mc"
            if self.check_hand_card(type):
                total = sum(evaluation)
                if total > 0 and total - getattr(evaluation, "hand") > 50000:
                    if self.playable(type):
                        self.play(type, play = True)
                        return False
        return True

    # offer or accept trades
    def trade(self, offer):
        # TODO implement card trading options
        return False

    # send a card to the player left of you before knowing the card receiving, popping that card from the hand
    def send_card_left(self):
        # send any negative cards left, else the one with the minimum value
        # TODO sending cards left when paranoia cards are played
        return False