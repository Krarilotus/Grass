import Grass as G
import Player as P


class Card:
    """ abstract Card class, make sure every card has type and value """
    def __init__(self):
        self.type = ""
        self.value = 0


class MarketOpen(Card):
    """ open the market as long as you don't already have one """
    def __init__(self):
        super().__init__()
        self.type = "mo"

    @staticmethod
    def playable(player: P) -> bool:
        return not("mo" in [sc.type for sc in player.stash])

    def play(self, player:P, game: G):
        if self.playable(player=player):
            player.stash.append(self)
        else:
            game.waste.append(self)


class MarketClose(Card):
    """ close the market if the own stashed peddle and protected peddle is bigger than 50k and market is not heated """
    def __init__(self, game):
        super().__init__()
        self.type = "mc"

    @staticmethod
    def playable(player: P) -> bool:
        current_state = player.eval_self()
        market_cap = getattr(current_state, "stash") + getattr(current_state, "protected")
        return not player.heated() and market_cap >= 50000

    def play(self, player: P, game: G):
        if self.playable(player=player):
            game.score_round()
        else:
            game.waste.append(self)


class Peddle(Card):
    """ Play peddle on open non heated market """
    def __init__(self, value):
        super().__init__()
        self.type = "pd"
        self.value = value

    @staticmethod
    def playable(player: P) -> bool:
        return not player.heated() and player.check_stash_card("mo")

    def play(self, player: P, game: G):
        if self.playable(player=player):
            player.stash.append(self)
        else:
            game.waste.append(self)


class HeatOn(Card):
    """ Play Heat on cards however you like as long as someone has an open market """
    def __init__(self, value):
        super().__init__()
        self.type = "hn"
        self.value = value

    @staticmethod
    def playable(target: P) -> bool:
        return target.check_stash_card("mo")

    def play(self, game: G, target: P):
        if self.playable(target=target):
            target.hassle.append(self)
        else:
            game.waste.append(self)


class HeatOff(Card):
    """ Play heat off and pack it on top of your hassle pile, you won't need to worry no more! """
    def __init__(self, value):
        super().__init__()
        self.type = "hf"
        self.value = value

    def playable(self, player: P) -> bool:
        return player.heated() == self.value

    def play(self, player: P, game: G):
        if self.playable(player=player):
            player.hassle.append(self)
        else:
            game.waste.append(self)


class PayFine(Card):
    """ Play heat off and pack it on top of your hassle pile, you won't need to worry no more! """
    def __init__(self):
        super().__init__()
        self.type = "pf"
        self.value = 0

    @staticmethod
    def playable(player: P) -> bool:
        peddle_cards = [pd for pd in player.stash if pd.type == "pd"]
        return player.heated() and peddle_cards

    def play(self, player: P, game: G):
        if self.playable(player=player):
            player.hassle.append(self)
        else:
            game.waste.append(self)


class Nirvana(Card):
    """ Can always play Nirvana cards, but really its only 'played' properly if we already have a market """
    @staticmethod
    def playable(player: P) -> bool:
        return player.check_stash_card("mo")


class StoneHigh(Nirvana):
    """ With Stonehigh we take the lowest stashed peddle card of all our opponents """
    def __init__(self):
        super().__init__()
        self.type = "st"

    def play(self, player: P, game: G):
        if self.playable(player=player):
            player.hassle.append(self)
            for pl in game.players:
                peddle_card = pl.take_lowest_stash_card()
                if peddle_card:
                    player.stash.append(peddle_card)
            player.move()
        else:
            game.waste.append(self)
            player.move()


class Euphoria(Nirvana):
    """ Same as Stonehigh, just with the highest peddle cards """
    def __init__(self):
        super().__init__()
        self.type = "eu"

    def play(self, player: P, game: G):
        if self.playable(player=player):
            player.hassle.append(self)
            for pl in game.players:
                peddle_card = pl.take_highest_stash_card()
                if peddle_card:
                    player.stash.append(peddle_card)
            player.move()
        else:
            game.waste.append(self)
            player.move()


class Paranoia(Card):
    """ We can always play paranoia cards, but better opt not to! If so, we send one card left! """
    def __init__(self):
        super().__init__()

    @staticmethod
    def playable() -> bool:
        return True

    def play(self, player: P, game: G):
        # sending cards left
        sent_card_before = None
        for pl in game.players:
            sent_card_after = pl.send_card_left
            if sent_card_before:
                pl.hand.append(sent_card_before)
            sent_card_before = sent_card_after
        game.players[0].hand.append(sent_card_before)


class SoldOut(Paranoia):
    """ loose lowest stashed peddle card and loose 2 turns """
    def __init__(self):
        super().__init__()
        self.type = "ds"
        self.value = 25000

    def play(self, player: P, game: G):
        super().play(player, game)
        player.skips = 1
        peddle_card = player.take_lowest_stash_card()
        if peddle_card:
            game.waste.append(peddle_card)
        game.waste.append(self)


class DoubleCrossed(Paranoia):
    """ loose highest stashed peddle card and loose 2 turns """
    def __init__(self):
        super().__init__()
        self.type = "dc"
        self.value = 50000

    def play(self, player: P, game: G):
        super().play(player, game)
        player.skips = 2
        peddle_card = player.take_highest_stash_card()
        if peddle_card:
            game.waste.append(peddle_card)
        game.waste.append(self)


class UtterlyWipedOut(Paranoia):
    """ loose everything when played, that is in stash and hassle pile and loose 2 turns """
    def __init__(self):
        super().__init__()
        self.type = "du"
        self.value = 100000

    def play(self, player: P, game: G):
        super().play(player, game)
        player.skips = 2
        while player.stash:
            game.waste.append(player.stash.pop())
        while player.hassle:
            game.waste.append(player.hassle.pop())
        game.waste.append(self)


class Protection(Card):
    """ protection will replace peddle cards with protected peddle cards in our stash, its non-reversible """
    def __init__(self, value):
        super().__init__()
        self.type = "pr"
        self.value = value

    def playable(self, player: P):
        player.check_stash_for_protection("pd", self.value)

