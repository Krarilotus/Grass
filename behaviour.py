standard_eval = {
    "hand": {
        "MarketOpen": 7500,
        "MarketClosed": 55000,
        "Peddle5k": 4000,
        "Peddle25k": 15000,
        "Peddle50k": 30000,
        "Peddle100k": 15000,
        "HeatOn": 3000,
        "HeatOff": 45000,
        "PayFine": 0,
        "StoneHigh": 60000,
        "Euphoria": 120000,
        "SoldOut": -15000,
        "DoubleCrossed": -40000,
        "UtterlyWipedOut": -100000,
        "Protected25k": 25000,
        "Protected50k": 50000,
        "StealNeighborsPot": 60000,
        "TheBanker": 100000
    },
    "stash": {
        "MarketOpen": 0,
        "Peddle5k": 7500,
        "Peddle25k": 20000,
        "Peddle50k": 40000,
        "Peddle100k": 80000,
        "Protected25k": 25000,
        "Protected50k": 50000,
    },
    "status": {
        "ready": 0,
        "marked opened": 20000,
        "heated": -50000,
        "skip": -35000,
    }
}


class Behaviour:
    """
    Anything in here will define the values and behaviour of the player
    It will also be able to offer and accept trades
    """
    def __init__(self):
        self.concept_values = standard_eval
        self.believes = {}
        self.worth = 0


class SimpleMinded(Behaviour):
    def __init__(self):
        super().__init__()
