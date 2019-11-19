import os, time, sys

from classes.deck import Deck
from classes.card import Card
from classes.hand import Hand
import utils as util
import blackjack_strategy as bs

# Global Variables
first_card = 0
second_card = 1
max_card_height = 10

class Game:
	"""This is a class for controlling the operations of the blackjack game. 

	Attributes: 
        winnings (int) -- the amount of money the player has.
	"""
	def __init__(self):
		"""The constructor for the Game class."""
		self.winnings = 100

	def play(self):
		"""The main controller for playing the game of Blackjack."""

		play_again = True
			
		while play_again:

			self.deck = Deck()
			self.deck.shuffle()

			# Initialize player and dealer's hands
			self.player_hand = Hand()
			self.dealer_hand = Hand(isDealer = True)

			self.display_empty_game()

			self.player_hand.prompt_for_wager(self.winnings)
			self.winnings -= self.player_hand.wager  # remove wager from current winnings

			self.deal_cards()

			self.dealer_hand.cards[first_card].flip_face_down()  # flip dealer's first card face down
			
			self.display_state_of_game(self.player_hand)


			choice = 'n'  # holder value for choice variable
			
			# player must have enough money to wager and cards in equal rank to split his or her hand
			if (self.winnings > self.player_hand.wager) and (self.player_hand.cards[first_card].rank == self.player_hand.cards[second_card].rank):
				choice = util.get_valid_input('\nWould you like to split? (Y)es or (N)o?: ', ['y','n'], 'Not a valid response')
				if choice == 'y':
					self.split_hand()
					self.play_split_hand()

			if choice != 'y':  # player did not choose to split or did not have ability to
				self.player_turn(self.player_hand)
				
				# dealer only needs to play if player has not gone over 21 and does not have blackjack
				if self.player_hand.get_over_21_status():
					self.dealer_hand.cards[first_card].flip_face_up()
				elif self.player_hand.has_blackjack():
					self.dealer_hand.cards[first_card].flip_face_up()
				else:
					self.dealer_turn(self.player_hand)
				
				self.resolve_wager(self.player_hand)

				self.display_state_of_game(self.player_hand)


			if self.player_hand.is_split:  # print outcome of both hands
				print('\nThe dealer finished with a score of',self.dealer_hand.sum_of_cards)
				print('Your first hand finished with a score of', self.player_hand.sum_of_cards)
				self.display_final_outcome(self.player_hand)
				
				print('\nThe dealer finished with a score of',self.dealer_hand.sum_of_cards)
				print('You second hand finished with a score of', self.player_second_hand.sum_of_cards)
				self.display_final_outcome(self.player_second_hand)
			else:
				print('\nThe dealer finished with a score of',self.dealer_hand.sum_of_cards)
				print('You finished with a score of', self.player_hand.sum_of_cards)
				self.display_final_outcome(self.player_hand)


			response = util.get_valid_input('Would you like to play again? (Y)es or (N)o: ', ['y','n'], 'Not a valid response')
			
			if self.winnings == 0:
				print('Sorry, you ran out of money. Goodbye.')
			elif response == 'n':
				print('Thanks for playing. Goodbye.')
				break


	def deal_cards(self):
		"""Deal two cards to each the player and the dealer."""
		for i in range(2):  # deal cards back and forth like a real game
			self.player_hand.add_card(self.deck.deal_card())
			self.dealer_hand.add_card(self.deck.deal_card())

	def player_turn(self, hand):
		"""Execute the user/player's turn while recommending the best strategy for beating the dealer.

		Keyword Arguments:
			hand (Hand) -- the player's hand playing the current turn.
		"""
		again = True
		while again and not hand.get_over_21_status():
			
			if hand.has_blackjack():  # stop turn of player has blackjack
				break
			
			self.display_state_of_game(hand)
			self.recommend_strategy(hand)

			if hand.wager > self.winnings:  # If the user does not have enough funds. Don't allow him or her to double down
				choice = util.get_valid_input('\n(H)it or (S)tand?: ', ['h', 's'], 'Invalid choice. Please choose "H" to hit or "S" to stand')
			else:
				choice = util.get_valid_input('\n(H)it, (S)tand, or (D)ouble Down?: ', ['h', 's', 'd'], 'Invalid choice. Please choose "H" to hit or "S" to stand')
			
			if choice == 'h':
				hand.add_card(self.deck.deal_card())
			elif choice == 'd':
				# double wager
				self.winnings -= hand.wager
				hand.wager += hand.wager
				
				# add only one card to hand. Player may not hit again
				hand.add_card(self.deck.deal_card())
				again = False  
			elif choice == 's':
				again = False

			self.display_state_of_game(hand)

	def recommend_strategy(self, player_hand):
		"""Inform the user of the statistically best move to make based on his or her hand sum, and the dealer's single visible card.

		Keyword Arguments:
			player_hand (Hand) -- the player's hand playing the current turn.
		"""
		Ace = 'A'
		if (player_hand.cards[first_card].rank == player_hand.cards[second_card].rank) and len(player_hand.cards) < 3:  # player has a pair on the first turn
			strategy = bs.make_pair_recommendation(player_hand.cards[first_card].rank, self.dealer_hand.cards[second_card].rank) # always check the dealer's face-up card (second card)
		elif player_hand.cards[first_card].rank != Ace and player_hand.cards[second_card].rank != Ace:  # user does not have an ace
			strategy = bs.make_hard_total_recommendation(player_hand.sum_of_cards, self.dealer_hand.cards[second_card].rank)
		elif player_hand.cards[first_card].rank != Ace and player_hand.cards[second_card].rank == Ace and len(player_hand.cards) < 3:  # user has an ace and a non-ace in the first hand
			strategy = bs.make_soft_total_recommendation(player_hand.cards[first_card].rank, self.dealer_hand.cards[second_card].rank)
		elif player_hand.cards[first_card].rank == Ace and player_hand.cards[second_card].rank != Ace and len(player_hand.cards) < 3:   # user has an ace and a non-ace in the first hand
			strategy = bs.make_soft_total_recommendation(player_hand.cards[second_card].rank, self.dealer_hand.cards[second_card].rank)
		else:
			strategy = bs.make_hard_total_recommendation(player_hand.sum_of_cards, self.dealer_hand.cards[second_card].rank)
		print('\nThe recommended strategy is to:', strategy)


	def dealer_turn(self, player_hand):
		"""Execute the dealer/computer player's turn. A dealer must always hit on a hand value less than 17.

		Keyword Arguments:
			player_hand (Hand) -- the player's hand playing the current turn.
		"""
		self.dealer_hand.cards[first_card].flip_face_up()
		self.display_state_of_game(player_hand)
		again = True
		while again:
			if self.dealer_hand.sum_of_cards < 17:  # dealer must hit when under 17
				self.dealer_hand.add_card(self.deck.deal_card())
			else:
				again = False
			time.sleep(.50)
			self.display_state_of_game(player_hand)


	def display_final_outcome(self, player_hand):
		"""Determine the final outcome of the hand against the dealer's hand to display the appropriate message to the user.

		Keyword Arguments:
			player_hand (Hand) -- the player's hand playing the current turn.
		"""
		if player_hand.has_blackjack():
			print('\nCongratualtions! You got Blackjack. You WIN!\n')
		elif player_hand.get_over_21_status():
			print('\nYou went over 21. You LOSE!\n')
		elif self.dealer_hand.get_over_21_status():
			print('\nThe dealer went over 21. You WIN!\n')
		elif self.dealer_hand.sum_of_cards < player_hand.sum_of_cards:
			print('\nYou WIN!\n')
		elif player_hand.sum_of_cards < self.dealer_hand.sum_of_cards:
			print('\nYou LOSE!\n')
		else:
			print('\nTie! The game results in a PUSH.\n')


	def resolve_wager(self, player_hand):
		"""Calculate the amount the player won or lost, and adjust his or her winnings appropriately.

		Keyword Arguments:
			player_hand (Hand) -- the player's hand playing the current turn.
		"""
		if player_hand.has_blackjack():
			self.winnings += player_hand.wager * 3
			player_hand.reset_wager()
		elif player_hand.get_over_21_status():  # player lost
			player_hand.reset_wager()
		elif self.dealer_hand.get_over_21_status():  # player won
			self.winnings += player_hand.wager * 2
			player_hand.reset_wager()
		elif player_hand.sum_of_cards < self.dealer_hand.sum_of_cards:  # player lost
			player_hand.reset_wager()
		elif self.dealer_hand.sum_of_cards < player_hand.sum_of_cards:  # player won
			self.winnings += player_hand.wager * 2
			player_hand.reset_wager()
		else:  # game ended in a push
			self.winnings += player_hand.wager
			player_hand.reset_wager()

	def display_empty_game(self):
		"""Print two empty cards for both the dealer and the player, as will as the player's current funds and bet."""
		util.clear_window()
		lines = [''] * max_card_height
		for i in range(2):  # display 2 cards
			lines[0] += '┌─────────┐'
			lines[1] += '│         │'
			lines[2] += '│         │'
			lines[3] += '│         │'
			lines[4] += '│         │'
			lines[5] += '│         │'
			lines[6] += '│         │' 
			lines[7] += '│         │'
			lines[8] += '└─────────┘'
		for line in lines:
			print(line)
		for line in lines:
			print(line)
		print('\n   Funds: ${} | Bet: ${}'.format(self.winnings, 0))  # display wager

	def display_state_of_game(self, player_hand):
		"""Print the dealer's hand, player's hand, current funds, and current bet amount to the console.

		Keyword Arguments:
			player_hand (Hand) -- the player's hand playing the current turn.
		"""
		time.sleep(.20)
		util.clear_window()
		self.dealer_hand.display_hand()
		player_hand.display_hand()
		print('\n   Funds: ${} | Bet: ${}'.format(self.winnings, player_hand.wager))  # display wager	

	
	# Methods used for gameplay when user splits his or her hand

	def play_split_hand(self):
		"""Play the rest of the game using two hands for the player rather than one."""
		self.player_turn(self.player_hand)
		self.player_turn(self.player_second_hand)
		
		self.dealer_turn(self.player_second_hand)
		
		self.resolve_wager(self.player_hand)
		self.resolve_wager(self.player_second_hand)

		self.display_state_of_game(self.player_second_hand)  # show the updated winnings and null bet amount after completed

	def split_hand(self):
		""" Create a second hand with a wager equal to that of the first hand so the user can play using both hands."""
		self.player_second_hand = Hand()
		self.player_second_hand.add_card(self.player_hand.remove_last_card())  # remove card from hand one and give it to hand two
		
		self.player_hand.indicate_hand_is_split()
		self.player_second_hand.indicate_hand_is_split()

		# deal a card to each hand
		self.player_hand.add_card(self.deck.deal_card())
		self.player_second_hand.add_card(self.deck.deal_card())

		# double wager
		self.winnings -= self.player_hand.wager
		self.player_second_hand.wager += self.player_hand.wager