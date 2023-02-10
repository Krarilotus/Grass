from player import Player
from grass import Grass


class Action:
    """
    Any Action that players could do will be tracked by the game
    In Fact, the Action history alone should be sufficient to recreate a game to a specific point

    Types of actions:
    - skipping a turn
    - drawing a card
    - playing a card
    - showing a card
    - giving a card for receiving a card
    - exchanging tabled peddle
    - making an offer
    - agreeing, accepting, rejecting or retracting (to) an offer
    Actions should be possibly connected in a way that it should be possible to promise future
    actions based on conditional actions. So basically the declaration of reactions
    -> These promises will also be coded as offers

    Offers should not be recursively stacked for no reason. So for any additional layer of nesting,
    at least one additional 'real' action (playing or trading a card) must be added to an offer!

    TODO: It should also be possible to lie for players with their offers!

    Actions can be checked if viable and if so they can always be executed.
    -> Make sure to check viability first in the case that you are unsure!
    """

    def __init__(self, player: Player):
        self.player = player
        self.time = -1

    def effect(self, game: Grass):
        self.time = game.turn

    def viable(self, game: Grass):
        return True


class Skip(Action):
    """ skipping your turn is boring, but it's a valid action """

    def __init__(self, player: Player):
        super().__init__(player)

    def effect(self, game: Grass):
        super().effect(game)
        self.player.skips -= 1

    def viable(self, game: Grass):
        return self.player.skips > 0


class DrawCard(Action):
    """ The player draws a card either from the deck or the waste pile, specified as pile """
    def __init__(self, player: Player, pile: str = "deck"):
        super().__init__(player)
        self.pile = pile

    def effect(self, game: Grass):
        super().effect(game)
        self.player.hand.append(getattr(game, self.pile).pop())

    def viable(self, game: Grass):
        if self.pile == "deck":
            return bool(game.deck)
        elif self.pile == "waste":
            return game.waste_status == "discarded"
        else:
            return False


class PlayCard(Action):
    """ playing a card, possible only if we have the card on hand """
    def __init__(self, player: Player, card_type: str, *args: list):
        super().__init__(player)
        self.card_type = card_type
        self.args = args

    def effect(self, game: Grass):
        super().effect(game)
        card = self.player.take_hand_card(self.card_type)
        card.play(*self.args)

    def viable(self, game: Grass):
        return self.player.check_hand_card(self.card_type)


class ShowCard(Action):
    """ Showing a card requires it to be in your hand! """
    def __init__(self, player: Player, card_type: str):
        super().__init__(player)
        self.card_type = card_type

    def effect(self, game: Grass):
        super().effect(game)

    def viable(self, game: Grass):
        return self.player.check_hand_card(self.card_type)


class CardTrade(Action):
    """ Trading a card for another card requires both players to have a card of the specified type! """
    def __init__(self, player: Player, target: Player, my_card_type: str, your_card_type: str):
        super().__init__(player)
        self.target = target
        self.my_card_type = my_card_type
        self.your_card_type = your_card_type

    def effect(self, game: Grass):
        super().effect(game)
        self.player.hand.append(self.target.take_hand_card(self.your_card_type))
        self.target.hand.append(self.player.take_hand_card(self.my_card_type))

    def viable(self, game: Grass):
        return self.player.check_hand_card(self.my_card_type) and self.target.check_hand_card(self.your_card_type)


class GivePeddle(Action):
    """ Giving a paddle card from the players stash only works when both markets aren't heated and open! """
    def __init__(self, player: Player, target: Player, cvalue: int):
        super().__init__(player)
        self.target = target
        self.cvalue = cvalue

    def effect(self, game: Grass):
        super().effect(game)
        self.target.stash.append(self.player.take_stash_card(self.cvalue))

    def viable(self, game: Grass):
        markets = self.player.check_stash_card("mo") and self.target.check_stash_card("mo")
        heat = not self.player.heated() and not self.target.heated()
        peddle = self.player.check_stash_card("pd", self.cvalue)
        return markets and heat and peddle


class Offer(Action):
    """
    Offers consist of multiple actions that need more than one player to work out
    Offers also come with Threats, which are actions the player threatens, if
    the offer isn't taken. Of course, smart players will check all targets for the
    offer and know, that threats could be empty, if more than one player shall for example
    be hit by the same heat threat.
    """
    def __init__(self, player: Player, target: Player, actions: list[Action], threats: list[Action]):
        super().__init__(player)
        self.actions = actions
        self.threats = threats
        self.target = target


class AgreeOffer(Action):
    """
    If you want to tell a player, that you'll take the offer whenever you got the chance to
    do so. This could be a reaction to an offer like: Give me Open Market for 5000 peddle.
    This is only really taking any effect for offers that aren't viable currently but would
    be in the future if some conditions are met. Other than that, nothing happens!
    """
    def __init__(self, player: Player, offer: Offer):
        super().__init__(player)
        self.offer = offer

    def effect(self, game: Grass):
        super().effect(game)

    def viable(self, game: Grass):
        return True


class AcceptOffer(Action):
    """
    A player can only check viability of a trade if they would accept them which
    needs to occur on their or the other players turn, who posed the offer
    However, a player can also make an offer when it is not their turn turing trading phase
    Also to accept an offer, all actions of that offer need to be viable
    and the player needs to be the target of said offer
    """
    def __init__(self, player: Player, offer: Offer):
        super().__init__(player)
        self.offer = offer

    def effect(self, game: Grass):
        super().effect(game)
        for ac in self.offer.actions:
            game.handle_action(ac)

    def viable(self, game: Grass):
        if self.player is self.offer.target:
            for ac in self.offer.actions:
                if not ac.viable(game):
                    return False
            return True
        else:
            return False


class RejectOffer(Action):
    """
    The rejecting player needs to be a target of an offer to reject it
    The rejection is only important for the games offer handling, so it can track
    which offers are still open and which aren't
    It is likely, that offers get automatically rejected after a player who was
    target of an offer took their turn without accepting it
    """
    def __init__(self, player: Player, offer: Offer):
        super().__init__(player)
        self.offer = offer

    def effect(self, game: Grass):
        super().effect(game)

    def viable(self, game: Grass):
        return self.player is self.offer.target


class RetractOffer(Action):
    """
    Retracting an offer can especially be smart if a player doesn't want to get called out
    on their bluff. However, if players already agreed to an offer prematurely
    (which they could also just forget about) it might not shine a bright light on them...
    """
    def __init__(self, player: Player, offer: Offer):
        super().__init__(player)
        self.offer = offer

    def effect(self, game: Grass):
        super().effect(game)

    def viable(self, game: Grass):
        return self.player is self.offer.player

