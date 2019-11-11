'''
	Notes:
		* need to make sure recommendations doesn't say to split twice
		* REMOVE ALL ACCESSOR FUNCTIONS!

	Make winnings global, and give the wager functions to hand

'''
import os
import time
import sys

#sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')

from Classes.deck import Deck
from Classes.card import Card
from Classes.hand import Hand
from strategyTables import hard_totals, soft_totals, pair_splitting
from utils import *


# The main controller

# Global Variables
first_card = 0
second_card = 1

class Game:

	def __init__(self):
		self.winnings = 100

	def play(self):

		play_again = True
			
		while play_again:

			self.deck = Deck()
			self.deck.shuffle()

			# Initialize player and dealer's hands
			self.player_hand = Hand()
			self.dealer_hand = Hand(isDealer = True)

			self.display_state_of_game(empty=True)

			self.player_hand.get_valid_wager(self.winnings)
			self.winnings -= self.player_hand.wager  # remove wager from current winnings

			self.deal_cards()

			self.dealer_hand.cards[first_card].flip_face_down()  # flip first dealer card face down
			clear_window()
			self.display_state_of_game(self.player_hand)


			choice = 'n'
			# player must have enough money to wager on a split and cards in equal rank
			if self.winnings > self.player_hand.wager and self.card_rank_equal(self.player_hand.cards[first_card], self.player_hand.cards[second_card]):
				choice = get_valid_input('\nWould you like to split? (Y)es or (N)o', ['y','n'], 'Not a valid response')
				if choice == 'y':
					self.split_hand()
					self.play_split_hand()

			if choice != 'y':
				self.player_turn(self.player_hand)
				if not self.player_hand.get_over_21_status():
					self.dealer_turn(self.player_hand)
					self.resolve_wager(self.player_hand)
					self.display_state_of_game(self.player_hand)
				else:  # no need for dealer to play
					self.dealer_hand.cards[first_card].flip_face_up()
					self.resolve_wager(self.player_hand)
					self.display_state_of_game(self.player_hand)


			print('\nYou finished with a score of', self.player_hand.get_sum_of_cards())
			print('The dealer finished with a score of',self.dealer_hand.get_sum_of_cards())
			if self.player_hand.is_split:
				self.display_final_outcome(self.player_hand)
				self.display_final_outcome(self.player_second_hand)
			else:
				self.display_final_outcome(self.player_hand)

			response = get_valid_input('\nWould you like to play again? (Y)es or (N)o: ', ['y','n'], 'Not a valid response')

			if self.winnings == 0:
				print('You ran out of money. Goodbye.')
			elif response == 'n':
				print('Thanks for playing. Goodbye.')
				break

	# Controllers
	def deal_cards(self):
		# deal cards back and forth
		for i in range(2):
			self.player_hand.add_card(self.deck.deal_card())
			self.dealer_hand.add_card(self.deck.deal_card())

	def card_rank_equal(self, card1, card2):
		if card1.rank == card2.rank:
			return True
		else:
			return False

	def player_turn(self, hand):
		again = True
		while again and not hand.get_over_21_status():
			clear_window()
			if hand.has_blackjack():  # stop turn of player has blackjack
				break
			self.display_state_of_game(hand)
			self.suggest_recommendation(hand)

			if hand.wager > self.winnings:  # If the user does not have enough funds. Don't allow him or her to double down
				choice = get_valid_input('\n(H)it or (S)tand?: ', ['h', 's'], 'Invalid choice. Please choose "H" to hit or "S" to stand')
			else:
				choice = get_valid_input('\n(H)it, (S)tand, or (D)ouble Down?: ', ['h', 's', 'd'], 'Invalid choice. Please choose "H" to hit or "S" to stand')
			
			if choice == 'h':
				hand.add_card(self.deck.deal_card())  # hit deck and add card to hand
				self.display_state_of_game(hand)
			elif choice == 'd':
				# double wager
				self.winnings -= hand.wager
				hand.wager += hand.wager
				self.display_state_of_game(hand)
				hand.add_card(self.deck.deal_card())  # hit deck and add card to hand
				self.display_state_of_game(hand)
				break
			elif choice == 's':
				break

	def dealer_turn(self, player_hand):
		self.dealer_hand.cards[first_card].flip_face_up()
		self.display_state_of_game(player_hand)
		again = True
		while again:
			if self.dealer_hand.get_sum_of_cards() < 17:  # dealer must hit when under 17
				self.dealer_hand.add_card(self.deck.deal_card())
			else:
				break
			self.display_state_of_game(player_hand)

	def display_state_of_game(self, hand=[], empty= False):
		clear_window()
		if empty:
			self.dealer_hand.display_empty_hand()  # dealer side
			self.player_hand.display_empty_hand()  # default to player since the hand will always exist	
			print('\n   Funds: ${} | Bet: ${}'.format(self.winnings, 0))  # display wager
		else:
			self.dealer_hand.display_hand()
			hand.display_hand()
			print('\n   Funds: ${} | Bet: ${}'.format(self.winnings, hand.wager))  # display wager	

	def suggest_recommendation(self, hand):
		Ace = 'A'
		if self.card_rank_equal(hand.cards[first_card], hand.cards[second_card]):
			strategy = self.make_pair_recommendation(hand)
		elif hand.cards[first_card].rank != Ace and hand.cards[second_card] != Ace: # always check the dealer's face-up card
			strategy = self.make_hard_total_recommendation(hand)
		elif hand.cards[first_card].rank != Ace and hand.cards[second_card] == Ace:
			strategy = self.make_soft_total_recommendation(hand, 0)
		elif hand.cards[first_card].rank == Ace and hand.cards[second_card] != Ace:
			strategy = self.make_soft_total_recommendation(hand, 1)
		print('\nThe recommended strategy is to:', strategy)

	def make_pair_recommendation(self, hand):
		if hand.is_split:
			strategy = self.make_hard_total_recommendation(hand)
		else:
			strategy = pair_splitting.get((hand.cards[first_card].rank, self.dealer_hand.get_visible_card_rank()))
		if strategy == None:
			strategy = 'Stand'
		return strategy

	def make_hard_total_recommendation(self, hand):
		strategy = hard_totals.get((hand.get_sum_of_cards(), self.dealer_hand.get_visible_card_rank()))
		if strategy == None and hand.get_sum_of_cards() < 8:
			strategy = 'Hit'
		elif strategy == None and hand.get_sum_of_cards() > 17:
			strategy = 'Stand'
		return strategy

	def make_soft_total_recommendation(self, hand, non_ace_index):
		strategy = soft_totals.get((hand.cards[non_ace_index].rank, self.dealer_hand.get_visible_card_rank()))
		return strategy

	def display_final_outcome(self, hand):
		if hand.has_blackjack():
			print('Congratualtions! You got Blackjack. You WIN!')
		elif hand.get_over_21_status():
			print('\nYou went over 21. You LOSE!')
		elif self.dealer_hand.get_over_21_status():
			print('\nThe dealer went over 21. You WIN!')
		elif self.dealer_hand.get_sum_of_cards() < hand.get_sum_of_cards():
			print('\nYou WIN!')
		elif hand.get_sum_of_cards() < self.dealer_hand.get_sum_of_cards():
			print('\nYou LOSE!')
		else:
			print('\nTie! The game results in a PUSH.')

	def resolve_wager(self, hand):
		if hand.has_blackjack():
			self.winnings += hand.wager * 3
			hand.reset_wager()
		elif hand.get_over_21_status():  # player lost
			hand.reset_wager()
		elif self.dealer_hand.get_over_21_status():  # player won
			self.winnings += hand.wager * 2
			hand.reset_wager()
		elif hand.get_sum_of_cards() < self.dealer_hand.get_sum_of_cards():  # player lost
			hand.reset_wager()
		elif self.dealer_hand.get_sum_of_cards() < hand.get_sum_of_cards():  # player won
			self.winnings += hand.wager * 2
			hand.reset_wager()
		else:  # push
			self.winnings += hand.wager
			hand.reset_wager()

	def play_split_hand(self):
		self.player_turn(self.player_hand)
		self.player_turn(self.player_second_hand)
		self.dealer_turn(self.player_second_hand)
		self.resolve_wager(self.player_hand)
		self.resolve_wager(self.player_second_hand)
		self.display_state_of_game(self.player_hand)
		self.display_state_of_game(self.player_second_hand)

	def split_hand(self):
		self.player_hand.indicate_hand_is_split()
		self.player_second_hand = Hand()
		self.player_second_hand.add_card(self.player_hand.remove_last_card())  # remove card from hand 1 and give to hand 2	
		self.player_second_hand.indicate_hand_is_split()

		# deal a card to each hand
		self.player_hand.add_card(self.deck.deal_card())
		self.player_second_hand.add_card(self.deck.deal_card())

		# double wager
		self.winnings -= self.player_hand.wager
		self.player_second_hand.wager += self.player_hand.wager

