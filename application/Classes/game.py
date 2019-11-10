import os
import time
import sys

#sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')

from Classes.deck import Deck
from Classes.card import Card
from Classes.hand import Hand
from Classes.wager import Wager
from strategyTables import hard_totals, soft_totals, pair_splitting
from utils import *


# The main controller

# Global Variables
first_card = 0
second_card = 1

class Game:

	def __init__(self):
		pass

	def play(self):

		self.wager = Wager()

		play_again = True
			
		while play_again:
			
			self.deck = Deck()
			self.deck.shuffle()

			# Initialize player and dealer's hands
			self.player_hand = Hand()
			self.dealer_hand = Hand(isDealer = True)

			self.display_empty_game()

			self.wager.make_wager()

			clear_window()

			self.deal_cards()

			self.dealer_hand.cards[first_card].flip_face_down()  # flip first dealer card face down
			self.display_state_of_game(self.player_hand)

			time.sleep(3)

			# test split here
			self.split_hand()
			self.play_split_hand()


			time.sleep(10)

			if self.check_for_any_blackjack():
				self.resolve_wager(self.player_hand)
				self.dealer_hand.cards[first_card].flip_face_up()
				self.display_state_of_game(self.player_hand)
				self.display_final_outcome()
			elif self.card_rank_equal(self.player_hand.cards[first_card], self.player_hand.cards[second_card]):
				choice = get_valid_input('\nWould you like to split? ', ['y','n'], 'Not a valid response')
				if choice == 'y':
					self.split_hand()
					self.play_split_hand()
				else:
					self.player_turn()
					if not self.player_hand.get_over_21_status():
						self.dealer_turn()
					else:
						self.dealer_hand.cards[first_card].flip_face_up()
			else:
				self.player_turn(self.player_hand)
				if not self.player_hand.get_over_21_status():
					self.dealer_turn(self.player_hand)
				else:
					self.dealer_hand.cards[first_card].flip_face_up()

				self.resolve_wager(self.player_hand)
				self.display_state_of_game(self.player_hand)
				print('\nYou finished with a score of', self.player_hand.sum_of_cards)
				print('The dealer finished with a score of',self.dealer_hand.sum_of_cards)
				self.display_final_outcome()

			response = get_valid_input('\nWould you like to play again? (Y)es or (N)o: ', ['y','n'], 'Not a valid response')

			if self.wager.get_current_value_owned() == 0:
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

	def player_turn(self, hand):
		again = True
		while again and not hand.get_over_21_status():
			self.display_state_of_game(hand)
			self.suggest_recommendation(hand)
			if self.wager.get_current_wager() > self.wager.get_current_value_owned():  # If the user does not have enough funds. Don't allow him or her to double down
				choice = get_valid_input('\n(H)it or (S)tand?: ', ['h', 's'], 'Invalid choice. Please choose "H" to hit or "S" to stand')
			else:
				choice = get_valid_input('\n(H)it, (S)tand, or (D)ouble Down?: ', ['h', 's', 'd'], 'Invalid choice. Please choose "H" to hit or "S" to stand')
			if choice == 'h':
				hand.add_card(self.deck.deal_card())  # hit deck and add card to hand
				self.display_state_of_game(hand)
			elif choice == 'd':
				self.wager.double_wager()
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
			if self.dealer_hand.sum_of_cards < 17:  # dealer must hit when under 17
				self.dealer_hand.add_card(self.deck.deal_card())
			elif self.dealer_hand.sum_of_cards < player_hand.sum_of_cards:  # if over 16 and losing to player
				self.dealer_hand.add_card(self.deck.deal_card())
			else:
				break
			self.display_state_of_game(player_hand)

	def display_final_outcome(self):
		if self.player_hand.get_blackjack_status():
			print('Congratualtions! You got Blackjack. You WIN!')
		elif self.dealer_hand.get_blackjack_status():
			print('The dealer has Blackjack. You LOSE!')
		elif self.player_hand.get_over_21_status():
			print('\nYou went over 21. You LOSE!')
		elif self.dealer_hand.get_over_21_status():
			print('\nThe dealer went over 21. You WIN!')
		elif self.dealer_hand.sum_of_cards < self.player_hand.sum_of_cards:
			print('\nYou WIN!')
		elif self.player_hand.sum_of_cards < self.dealer_hand.sum_of_cards:
			print('\nYou LOSE!')
		else:
			print('\nTie! The game results in a PUSH.')

	def resolve_wager(self, hand):
		if hand.get_blackjack_status():
			self.wager.collect_winnings(blackjack=True)
		elif hand.get_over_21_status():  # player lost
			self.wager.lose_wager()
		elif self.dealer_hand.get_over_21_status():  # player won
			self.wager.collect_winnings()
		elif hand.sum_of_cards < self.dealer_hand.sum_of_cards:  # player lost
			self.wager.lose_wager()
		elif self.dealer_hand.sum_of_cards < hand.sum_of_cards:  # player won
			self.wager.collect_winnings()
		else:  # push
			self.wager.return_wager_to_player()

	def check_for_any_blackjack(self):
		if self.player_hand.get_blackjack_status() or self.dealer_hand.get_blackjack_status():
			return True
		else:
			return False

	def display_state_of_game(self, hand):
		clear_window()
		self.dealer_hand.display_hand()
		hand.display_hand()
		self.wager.display_wager()

	def display_empty_game(self):
		clear_window()
		self.dealer_hand.display_empty_hand()  # dealer side
		self.player_hand.display_empty_hand()  # player side
		self.wager.display_wager()

	def suggest_recommendation(self, hand):
		Ace = 'A'
		if self.card_rank_equal(hand.cards[first_card], hand.cards[second_card]):
			strategy = self.make_pair_recommendation(hand)
		elif hand.cards[first_card].rank != Ace and hand.cards[second_card] != Ace: # always check the dealer's face-up card
			strategy = self.make_hard_total_recommendation(hand)
		elif hand.cards[first_card].rank != Ace and hand.cards[second_card] == Ace:
			strategy = self.make_soft_total_recommendation(hand, 1)
		elif hand.cards[first_card].rank == Ace and hand.cards[second_card] != Ace:
			strategy = self.make_soft_total_recommendation(hand, 0)
		print('\nThe recommended strategy is to:', strategy)

	def make_pair_recommendation(self, hand):
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

	def card_rank_equal(self, card1, card2):
		if card1.rank == card2.rank:
			return True
		else:
			return False


	def split_hand(self):
		""" Treat a split like the player has two hands
		"""
		#self.wager.double_wager() # need to add to the wager too
		self.wager.double_wager()
		self.player_second_hand = Hand()
		self.player_second_hand.add_card(self.player_hand.remove_last_card())  # remove card from hand 1 and give to hand 2	
		
		# deal a card to each hand
		self.player_hand.add_card(self.deck.deal_card())
		self.player_second_hand.add_card(self.deck.deal_card())


	def play_split_hand(self):
		self.player_turn(self.player_hand)
		self.player_turn(self.player_second_hand)

	def resolve_wager_on_split_hand(self):
		pass