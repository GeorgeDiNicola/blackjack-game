from Deck import Deck
from Card import Card
from Hand import Hand
from Wager import Wager
from strategyTables import hard_totals, soft_totals, pair_splitting
import os
import time

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
			
		while play_again and self.wager.get_current_value_owned() > 0:
			
			self.deck = Deck()
			self.deck.shuffle()

			# Initialize player and dealer's hands
			self.player_hand = Hand()
			self.dealer_hand = Hand(isDealer = True)

			self.display_empty_game()

			self.wager.make_wager()

			os.system('clear')  # only for mac and linux
			self.deal_cards()

			self.dealer_hand.cards[first_card].flip_face_down()  # flip first dealer card face down

			self.display_state_of_game()

			if self.card_rank_equal(self.player_hand.cards[first_card], self.player_hand.cards[second_card]):
				choice = self.get_valid_input('\nWould you like to split? ', ['y','n'], 'Not a valid response')

			if self.check_for_any_blackjack():
				self.update_wager()
				self.dealer_hand.cards[first_card].flip_face_up()
				self.display_state_of_game()
				self.display_final_outcome()
			else:
				# ask about split
				self.player_turn()
				if not self.player_hand.get_over_21_status():
					self.dealer_turn()
				else:
					self.dealer_hand.cards[first_card].flip_face_up()

				self.update_wager()
				self.display_state_of_game()
				print('\nYou finished with a score of', self.player_hand.sum_of_cards)
				print('The dealer finished with a score of',self.dealer_hand.sum_of_cards)
				self.display_final_outcome()

			response = self.get_valid_input('\nWould you like to play again? (Y)es or (N)o: ', ['y','n'], 'Not a valid response')

			if response == 'n':
				print('Thanks for playing. Goodbye.')
				break

	# Controllers
	def deal_cards(self):
		# deal cards back and forth
		for i in range(2):
			self.player_hand.add_card(self.deck.deal_card())
			self.dealer_hand.add_card(self.deck.deal_card())

	def player_turn(self):
		turn_number = 1
		again = True
		while again and not self.player_hand.get_over_21_status():
			self.suggest_recommendation()
			choice = self.get_valid_input('\n(H)it, (S)tand, or (D)ouble Down?: ', ['h', 's', 'd'], 'Invalid choice. Please choose "H" to hit or "S" to stand')
			if choice == 'h':
				self.player_hand.add_card(self.deck.deal_card())  # hit deck and add card to hand
				self.display_state_of_game()
			elif choice == 'd':
				self.wager.double_wager()
				self.display_state_of_game()
				self.player_hand.add_card(self.deck.deal_card())  # hit deck and add card to hand
				self.display_state_of_game()
				break
			elif choice == 's':
				break
			elif choice == 'y':  # indicates the user has two equal cards and wants to split
				self.split_hand()
				break
			turn_number += 1

	def dealer_turn(self):
		self.dealer_hand.cards[first_card].flip_face_up()
		self.display_state_of_game()
		again = True
		while again:
			if self.dealer_hand.sum_of_cards < 17:  # dealer must hit when under 17
				self.dealer_hand.add_card(self.deck.deal_card())
			elif self.dealer_hand.sum_of_cards < self.player_hand.sum_of_cards:  # if over 16 and losing to player
				self.dealer_hand.add_card(self.deck.deal_card())
			else:
				break
			self.display_state_of_game()

	#TODO move to a folder called "common"
	def get_valid_input(self, prompt, possible_input, error_message):
		valid = False
		while not valid:
			choice = input(prompt)
			if choice.lower() in possible_input:
				valid = True
			else:
				print(error_message)
		return choice.lower()


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

	def update_wager(self):
		if self.player_hand.get_blackjack_status():
			self.wager.collect_winnings(bßlackjack=True)
		elif self.player_hand.get_over_21_status():  # player lost
			self.wager.lose_wager()
		elif self.dealer_hand.get_over_21_status():  # player won
			self.wager.collect_winnings()
		elif self.player_hand.sum_of_cards < self.dealer_hand.sum_of_cards:  # player lost
			self.wager.lose_wager()
		elif self.dealer_hand.sum_of_cards < self.player_hand.sum_of_cards:  # player won
			self.wager.collect_winnings()
		else:  # push
			self.wager.return_wager_to_player()

	def check_for_any_blackjack(self):
		if self.player_hand.get_blackjack_status() or self.dealer_hand.get_blackjack_status():
			return True
		else:
			return False

	def display_state_of_game(self):
		os.system('clear')  # only for mac and linux
		self.dealer_hand.display_hand()
		self.player_hand.display_hand()
		self.wager.display_wager()

	def display_empty_game(self):
		os.system('clear')  # only for mac and linux
		self.dealer_hand.display_empty_hand()  # dealer side
		self.player_hand.display_empty_hand()  # player side
		self.wager.display_wager()

	def suggest_recommendation(self):
		Ace = 'A'
		if self.card_rank_equal(self.player_hand.cards[first_card], self.player_hand.cards[second_card]):
			strategy = self.make_pair_recommendation()
		elif self.player_hand.cards[first_card].rank != Ace and self.player_hand.cards[second_card] != Ace: # always check the dealer's face-up card
			strategy = self.make_hard_total_recommendation()
		elif self.player_hand.cards[first_card].rank != Ace and self.player_hand.cards[second_card] == Ace:
			strategy = self.make_soft_total_recommendation(1)
		elif self.player_hand.cards[first_card].rank == Ace and self.player_hand.cards[second_card] != Ace:
			strategy = self.make_soft_total_recommendation(0)
		print('\nThe recommended strategy is to:', strategy)

	def make_pair_recommendation(self):
		strategy = pair_splitting.get((self.player_hand.cards[first_card].rank, self.dealer_hand.get_visible_card_rank()))
		if strategy == None:
			strategy = 'Stand'
		return strategy

	def make_hard_total_recommendation(self):
		strategy = hard_totals.get((self.player_hand.get_sum_of_cards(), self.dealer_hand.get_visible_card_rank()))
		if strategy == None and self.player_hand.get_sum_of_cards() < 8:
			strategy = 'Hit'
		elif strategy == None and self.player_hand.get_sum_of_cards() > 17:
			strategy = 'Stand'
		return strategy

	def make_soft_total_recommendation(self, ace_index):
		strategy = soft_totals.get((self.player_hand.cards[ace_index].rank, self.dealer_hand.get_visible_card_rank()))
		return strategy

	def card_rank_equal(self, card1, card2):
		if card1.rank == card2.rank:
			return True
		else:
			return False

	def split_hand(self):
		""" Treat a split like the player has two hands
		"""
		self.wager.double_wager() # need to add to the wager too
		self.player_hand2 = Hand()
		self.player_hand2.add_card(self.player_hand.remove_top_card())  # remove card from hand 1 and give to hand 2	
		
		# deal a card to each hand
		self.player_hand.add_card(self.deck.deal_card())
		self.player_hand2.add_card(self.deck.deal_card())