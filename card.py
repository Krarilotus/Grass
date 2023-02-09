from grass import Grass
from player import Player


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
    def playable(player: Player) -> bool:
        return not ("mo" in [sc.type for sc in player.stash])

    def play(self, player: Player, game: Grass):
        if self.playable(player=player):
            player.stash.append(self)
        else:
            game.discard(self)


class MarketClose(Card):
    """ close the market if the own stashed peddle and protected peddle is bigger than 50k and market is not heated """

    def __init__(self):
        super().__init__()
        self.type = "mc"

    @staticmethod
    def playable(player: Player) -> bool:
        current_state = player.eval_self()
        market_cap = getattr(current_state, "stash") + getattr(current_state, "protected")
        return not player.heated() and market_cap >= 50000

    def play(self, player: Player, game: Grass):
        if self.playable(player=player):
            game.status = "closed"
        else:
            game.discard(self)


class Peddle(Card):
    """ Play peddle on open non-heated market """

    def __init__(self, value):
        super().__init__()
        self.type = "pd"
        self.value = value

    @staticmethod
    def playable(player: Player) -> bool:
        return not player.heated() and player.check_stash_card("mo")

    def play(self, player: Player, game: Grass):
        if self.playable(player=player):
            player.stash.append(self)
        else:
            game.discard(self)


class HeatOn(Card):
    """ Play Heat on cards however you like as long as someone has an open market """

    def __init__(self, value):
        super().__init__()
        self.type = "hn"
        self.value = value

    @staticmethod
    def playable(target: Player) -> Card:
        return target.check_stash_card("mo")

    def play(self, game: Grass, target: Player):
        if self.playable(target=target):
            target.hassle.append(self)
        else:
            game.discard(self)


class HeatOff(Card):
    """ Play heat off and pack it on top of your hassle pile, you won't need to worry no more! """

    def __init__(self, value):
        super().__init__()
        self.type = "hf"
        self.value = value

    def playable(self, player: Player) -> bool:
        return player.heated() == self.value

    def play(self, player: Player, game: Grass):
        if self.playable(player=player):
            player.hassle.append(self)
        else:
            game.discard(self)


class PayFine(Card):
    """ Play heat off and pack it on top of your hassle pile, you won't need to worry no more! """

    def __init__(self):
        super().__init__()
        self.type = "pf"
        self.value = 0

    @staticmethod
    def playable(player: Player, cvalue: int) -> int | list:
        return player.heated() and player.check_stash_card("pd", cvalue)

    def play(self, player: Player, game: Grass, cvalue: int):
        if self.playable(player, cvalue):
            game.burn(player.take_stash_card(cvalue))
            player.hassle.append(self)
        else:
            game.discard(self)


class Nirvana(Card):
    """ Can always play Nirvana cards, but really its only 'played' properly if we already have a market """

    @staticmethod
    def playable(player: Player) -> Card:
        return player.check_stash_card("mo")


class StoneHigh(Nirvana):
    """ With StoneHigh, we take the lowest stashed peddle card of all our opponents """

    def __init__(self):
        super().__init__()
        self.type = "st"

    def play(self, player: Player, game: Grass):
        if self.playable(player=player):
            player.hassle.append(self)
            for pl in game.players:
                peddle_card = pl.take_lowest_stash_card()
                if peddle_card:
                    player.stash.append(peddle_card)
            player.move()
        else:
            game.discard(self)
            player.move()


class Euphoria(Nirvana):
    """ With Euphoria, we take the highest stashed peddle card of all our opponents """

    def __init__(self):
        super().__init__()
        self.type = "eu"

    def play(self, player: Player, game: Grass):
        if self.playable(player=player):
            player.hassle.append(self)
            for pl in game.players:
                peddle_card = pl.take_highest_stash_card()
                if peddle_card:
                    player.stash.append(peddle_card)
            player.move()
        else:
            game.discard(self)
            player.move()


class Paranoia(Card):
    """ We can always play paranoia cards, but better opt not to! If so, we send one card left! """

    def __init__(self):
        super().__init__()

    @staticmethod
    def playable() -> bool:
        return True

    def play(self, player: Player, game: Grass):
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

    def play(self, player: Player, game: Grass):
        super().play(player, game)
        player.skips = 1
        peddle_card = player.take_lowest_stash_card()
        if peddle_card:
            game.burn(peddle_card)
        game.burn(self)


class DoubleCrossed(Paranoia):
    """ loose highest stashed peddle card and loose 2 turns """

    def __init__(self):
        super().__init__()
        self.type = "dc"
        self.value = 50000

    def play(self, player: Player, game: Grass):
        super().play(player, game)
        player.skips = 2
        peddle_card = player.take_highest_stash_card()
        if peddle_card:
            game.burn(peddle_card)
        game.burn(self)


class UtterlyWipedOut(Paranoia):
    """ loose everything when played, that is in stash and hassle pile and loose 2 turns """

    def __init__(self):
        super().__init__()
        self.type = "du"
        self.value = 100000

    def play(self, player: Player, game: Grass):
        super().play(player, game)
        player.skips = 2
        while player.stash:
            game.burn(player.stash.pop())
        while player.hassle:
            game.burn(player.hassle.pop())
        game.burn(self)


class Protected(Card):
    """ protection will replace peddle cards with protected peddle cards in our stash, its non-reversible """

    def __init__(self, value):
        super().__init__()
        self.type = "pr"
        self.value = value

    def playable(self, player: Player):
        return not player.heated() and player.check_stash_for_protection(self.value)

    def play(self, player: Player, game: Grass):
        if self.playable(player):
            player.stash = [c for i, c in enumerate(player.stash)
                            if i not in player.check_stash_for_protection(self.value)]
            player.stash.append(self)
        else:
            game.discard(self)


class StealNeighborsPot(Card):
    """ Steal a specific target value from any other player, that is unprotected if our own market isn't heated """

    def __int__(self):
        super().__init__()
        self.type = "sn"

    @staticmethod
    def playable(player: Player, target: Player, cvalue: int):
        return not player.heated() and target.check_stash_card("pd", cvalue)

    def play(self, player: Player, game: Grass, target: Player, cvalue: int):
        if self.playable(player, target, cvalue):
            player.stash.append(target.take_stash_card(cvalue))
            game.burn(self)
        else:
            game.discard(self)


class TheBanker(Card):
    """ Nobody really would want to play this card, if they play it, it will just be discarded """

    def __int__(self):
        super().__init__()
        self.type = "ba"

    @staticmethod
    def playable():
        return False

    def play(self, game: Grass):
        game.discard(self)
