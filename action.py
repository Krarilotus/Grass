from card import *
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
    - accepting, rejecting or retracting and offer
    Actions should be possibly connected in a way that it should be possible to promise future
    actions based on conditional actions. So basically the declaration of reactions
    -> These promises will also be coded as offers

    Offers should not be recursively stacked for no reason. So for any additional layer of nesting,
    at least one additional 'real' action (playing or trading a card) must be added to an offer!

    It should also be possible to lie for players with their offers!

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


    def viable(self, game: ):









class Offer(Action):
    def __init__(self, player: Player, conditions: list[Action], actions: list[Action]):
        super().__init__(player)
        self.conditions = conditions
        self.actions = actions

