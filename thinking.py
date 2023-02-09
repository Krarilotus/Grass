from player import Player


class Thinking:
    """
    This class contains all the rules that the player has for
    deriving information from the flow of the game
    -> It also offers guidance to use the behaviour component to
    create believes
    -> In here are defined multiple concepts, that just get updated
    whenever anything that influences them gets triggered
    In this sense, the Thinking component is always updated whenever a player
    moves themselves, or it is another players trading phase
    """
    def __init__(self, player: Player):
        self.player = player
        self.concepts = {self.player.behaviour.believes}
