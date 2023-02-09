# Grass - The intoxicating new card game
This game is mostly based on luck but over time a lot of strategy takes effect and especially the ability to make promises and trade between players adds a lot of depth for gametheoretical analysis.
This project aims to replicate the game with some applied houserules and make it possible to develop AIs to play the game with and simulate games to find good strategies!

## Gamerules:
### Setup:
Every round, the stack of 104 cards per 10 players is shuffled, then each player is given 6 hand cards, the rest is set aside face down as the drawing  pile. The top card of the drawing pile is flipped to start the wasted pile. The card dealer job is forwarded clockwise between rounds.
### Game:
The player take turns in clockwise order, with the player left of the dealer starting. The player can either draw the top discarded card from the wasted pile, or the top facedown card from the draw pile. The player may then trade any number of hand cards for the same number of handcards with other players, or trade tabled peddle cards between open markets between himself and other players. The player may also trade promises of future trades, making conditional statements.  
The player ends their turn by playing one card from their hand on their respective location to play on, dealing the effect of the card.
A player might skip their turn or play another turn right away depending on their last played card.
### Scoring:
As soon as one player plays the 'Market Closed' card after meeting its condition, the Round is scored. The market is also closed if a player takes their turn without the ability to draw a card. Each player adds up the value of their protected and unprotected stash, substracting 20% of the unprotected stash if any of the other players holds the banker, and also substracting values of all the peddle and paranoia cards from their hands. If a player holds the banker themselves, they take the 20% substracted from the unprotected peddle cards off of the other players and add that to their own sum. The sum of these values for each player is then added to their overall gamescore.
### Winning the game:
The game ends, if the overall score of one or more players exceeds 250k. The player with the highest score wins the game. If multiple players have the highest score, the game ends in a draw.
