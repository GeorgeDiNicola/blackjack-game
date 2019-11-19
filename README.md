# Blackjack Game with Decision Assistant

A terminal-based Blackjack game with a built-in decision assistant that recommends the statistically best move to the user during every turn.

<img src="https://media.giphy.com/media/cnuv9TbEAA8NN4h6c5/giphy.gif" width="576" height="401" />

# How to play Blackjack:

The objective of the game is to beat the dealer. To beat the dealer, the sum of the cards in your hand will need to be greater than the sum of the cards in the dealer's hand, without being over 21. If you reach a sum over 21, you lose. If the dealer reaches a sum over 21 (and you have not), then you win.

For more information about how to play Blackjack: https://bicyclecards.com/how-to-play/blackjack/ <br/>
Note: This game does NOT allow the player to purchase insurance. 

# How to play in the terminal
- The game initializes with the player having $100 to spend betting on the game.
- The game will begin by asking for a wager. You may choose to wager $1, $5, $10, or $20 (when you type these, do NOT type the dollar sign). 
- If the first two cards you receive have an equal rank (ex: "Q" and "Q"), then you will be asked if you would like to split. Inputting the letter "Y" will allow you to split and from then on you will play using two hands. In addition your wager will double since the newly dealt hand will need to match the wager you initially made. If you choose "N" to indicate no, then the game will go on as normal (using one hand). You may only split once during the game.
- If the first two cards you receive are not equal in rank, then you will be asked if you would like to Hit (H), Stand (S), or Double Down (D). Above the prompt, the game's decision assistant will suggest the best choice to make based on probablitiy of winning.
