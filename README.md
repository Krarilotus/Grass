# Grass - The intoxicating new card game
This game is mostly based on luck but over time a lot of strategy takes effect and especially the ability to make promises and trade between players adds a lot of depth for gametheoretical analysis.
This project aims to replicate the game with some applied houserules and make it possible to develop AIs to play the game with and simulate games to find good strategies!

## Gamerules:
### Game itself:
#### Setup:
Every round, the stack of 104 cards per 10 players is shuffled, then each player is given 6 hand cards, the rest is set aside face down as the drawing  pile. The top card of the drawing pile is flipped to start the wasted pile. The card dealer job is forwarded clockwise between rounds.
#### Game:
The player take turns in clockwise order, with the player left of the dealer starting. The player can either draw the top discarded card from the wasted pile, or the top facedown card from the draw pile. The player may then trade any number of hand cards for the same number of handcards with other players, or trade tabled peddle cards between open markets between himself and other players. The player may also trade promises of future trades, making conditional statements.  
The player ends their turn by playing one card from their hand on their respective location to play on, dealing the effect of the card.
A player might skip their turn or play another turn right away depending on their last played card.
#### Scoring:
As soon as one player plays the 'Market Closed' card after meeting its condition, the Round is scored. The market is also closed if a player takes their turn without the ability to draw a card. Each player adds up the value of their protected and unprotected stash, substracting 20% of the unprotected stash if any of the other players holds the banker, and also substracting values of all the peddle and paranoia cards from their hands. If a player holds the banker themselves, they take the 20% substracted from the unprotected peddle cards off of the other players and add that to their own sum. The sum of these values for each player is then added to their overall gamescore.
#### Winning the game:
The game ends, if the overall score of one or more players exceeds 250k. The player with the highest score wins the game. If multiple players have the highest score, the game ends in a draw.

### Cards:
One Deck of cards contains 104 total cards. Their usecases and effects are defined below:
#### Market Open (10x)
Opens the market for the player, can only be played if the market isn't open already
#### Market Closed (5x)
closes the market for everyone and ends a round to score points, needs 50k in the stash of the player and can't be played while heated
#### Peddle (12 x 5k, 10x 25k, 5x 50k, 1x 100k)
Can be played on the players stash if the market is open and not heated. They count positively towards the players score if on stash and negative if on the players hand while scoring for the game. They can also be traded between players stashes as long as none of the parties trading is heated. They  can be stolen even if the market stolen from is heated
#### HeatOn (4 types a 3 cards)
Can be played on any players hassle pile to blockade their moves, which prevents them from stealing single peddle cards, playing their own peddle cards, trading peddle cards or protecting their peddle cards. It also prevents them from closing the market. You can play a 2nd heat on a player, which then takes the top spot on the hassle pile and the previous heat won't be an issue anymore.
#### HeatOff (4 types a 5 cards)
Same as HeatOn HeatOff comes in 4 different types which corresponds to the HeatOn types. Only a matchign heatOff can remove the corresponding HeatOn. It is played on a players hasslepile if matching with the top heatOn covering it and reopening the market
#### PayFine (4x)
This HeatOff works for any heat on your market, but it requires the player to pay by burning one of the tabled peddle cards from their stash.
#### Nirvana (5x StoneHigh, 1x Euphoria)
These cards remove any heat from the players market, take the least (StoneHigh) or the highest (Euphoria) unprotected peddlecard from all other players stashes and give the player anopther turn. This is truely OP and players usually wait for a very good time to play these!
#### Paranoia (4x SoldOut, 3x DoubleCrossed, 1x UtterlyWipedOut)
Each of these lets all players give one hand card to the left. They also loose you the least (Sold out) the highest (DoubleCrossaed) peddle from your tabled peddle or even the entire stash, including your opened market (UtterlyWipedOut). On top of that they make the player skip their next 1 (SoldOut) or 2 (DC, UWO) turns
#### Protected (2x 50k, 4x 25k)
They can be played if the market is not heated and the respective value in peddle cards is exactly met by either one or a combination of unprotected peddlecards from your stash. Then they get protected and will not be stealable nor taken by the banker in the end anymore.
#### StealNeighborsPot (4x)
This skim card lets the player take any open tabled peddle card from any other player as long as your own market is open and not heated. It is then put directly the players stash
#### TheBanker (1x)
This card is held in the hand until the game finishes.. If played, it is only discarded without an effect. It grants the holder 20% of all unprotected peddle on the board, which will be added to their score and substracted from the income of the other players respectively

