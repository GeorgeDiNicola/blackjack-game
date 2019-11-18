import os, time, sys

from Classes.deck import Deck
from Classes.card import Card
from Classes.hand import Hand
from utils import *

# Global Variables
first_card = 0
second_card = 1
max_card_height = 10

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

			self.display_empty_game()

			self.player_hand.prompt_for_wager(self.winnings)
			self.winnings -= self.player_hand.wager  # remove wager from current winnings

			self.deal_cards()

			self.dealer_hand.cards[first_card].flip_face_down()  # flip first dealer card face down
			
			self.display_state_of_game(self.dealer_hand, self.player_hand)

			choice = 'n'  # holder value for choice variable
			
			# player must have enough money to wager and cards in equal rank to split his or her hand
			if (self.winnings > self.player_hand.wager) and (self.player_hand.cards[first_card] == self.player_hand.cards[second_card]):
				choice = get_valid_input('\nWould you like to split? (Y)es or (N)o?: ', ['y','n'], 'Not a valid response')
				if choice == 'y':
					self.split_hand()
					self.play_split_hand()

			if choice != 'y':  # player did not choose to split or did not have ability to
				self.player_turn(self.player_hand)
				
				# dealer only needs to play if player has not gone over 21 and does not have blackjack
				if not (self.player_hand.get_over_21_status() or self.player_hand.has_blackjack == False):
					self.dealer_turn(self.player_hand)
				else:
					self.dealer_hand.cards[first_card].flip_face_up()
				
				self.resolve_wager(self.player_hand)

				self.display_state_of_game(self.dealer_hand, self.player_hand)


			if self.player_hand.is_split:
				print('\nYour first hand finished with a score of', self.player_hand.get_sum_of_cards())
				print('The dealer finished with a score of',self.dealer_hand.get_sum_of_cards())
				self.display_final_outcome(self.player_hand)
				
				print('You second hand finished with a score of', self.player_second_hand.get_sum_of_cards())
				print('The dealer finished with a score of',self.dealer_hand.get_sum_of_cards())
				self.display_final_outcome(self.player_second_hand)
			else:
				print('\nYou finished with a score of', self.player_hand.get_sum_of_cards())
				print('The dealer finished with a score of',self.dealer_hand.get_sum_of_cards())
			
			if self.player_hand.is_split:  # display outcome for both hands the player has
				self.display_final_outcome(self.player_hand)
				self.display_final_outcome(self.player_second_hand)
			else:
				self.display_final_outcome(self.player_hand)


			response = get_valid_input('\nWould you like to play again? (Y)es or (N)o: ', ['y','n'], 'Not a valid response')
			
			if self.winnings == 0:
				print('Sorry, you ran out of money. Goodbye.')
			elif response == 'n':
				print('Thanks for playing. Goodbye.')
				break

	def deal_cards(self):
		# deal cards back and forth like a real game
		for i in range(2):
			self.player_hand.add_card(self.deck.deal_card())
			self.dealer_hand.add_card(self.deck.deal_card())

	def player_turn(self, hand):
		again = True
		while again and not hand.get_over_21_status():
			
			if hand.has_blackjack():  # stop turn of player has blackjack
				break
			
			self.display_state_of_game(self.dealer_hand, hand)
			self.recommend_strategy(hand)

			if hand.wager > self.winnings:  # If the user does not have enough funds. Don't allow him or her to double down
				choice = get_valid_input('\n(H)it or (S)tand?: ', ['h', 's'], 'Invalid choice. Please choose "H" to hit or "S" to stand')
			else:
				choice = get_valid_input('\n(H)it, (S)tand, or (D)ouble Down?: ', ['h', 's', 'd'], 'Invalid choice. Please choose "H" to hit or "S" to stand')
			
			# evaluate the choice given by the player
			if choice == 'h':
				hand.add_card(self.deck.deal_card())  # hit deck and add card to hand
				self.display_state_of_game(self.dealer_hand, hand)
			elif choice == 'd':
				# double wager
				self.winnings -= hand.wager
				hand.wager += hand.wager
				
				hand.add_card(self.deck.deal_card())  # hit deck and add card to hand
				self.display_state_of_game(self.dealer_hand, hand)
				again = False  # can only hit once after doubling down
			elif choice == 's':
				again = False

	def dealer_turn(self, player_hand):
		self.dealer_hand.cards[first_card].flip_face_up()
		self.display_state_of_game(self.dealer_hand, player_hand)
		again = True
		while again:
			if self.dealer_hand.get_sum_of_cards() < 17:  # dealer must hit when under 17
				self.dealer_hand.add_card(self.deck.deal_card())
			else:
				again = False
			self.display_state_of_game(self.dealer_hand, player_hand)
		#self.display_state_of_game(self.dealer_hand, player_hand)

	def recommend_strategy(self, hand):
		Ace = 'A'
		if (hand.cards[first_card] == hand.cards[second_card]) and len(hand.cards) < 3:
			strategy = make_pair_recommendation(hand.cards[first_card].rank, self.dealer_hand.get_visible_card_rank())
		elif hand.cards[first_card].rank != Ace and hand.cards[second_card] != Ace: # always check the dealer's face-up card
			strategy = make_hard_total_recommendation(hand.get_sum_of_cards(), self.dealer_hand.get_visible_card_rank())
		elif hand.cards[first_card].rank != Ace and hand.cards[second_card] == Ace:
			strategy = make_soft_total_recommendation(hand.cards[first_card].rank, self.dealer_hand.get_visible_card_rank())
		elif hand.cards[first_card].rank == Ace and hand.cards[second_card] != Ace:
			strategy = make_soft_total_recommendation(hand.cards[second_card].rank, self.dealer_hand.get_visible_card_rank())
		else:
			strategy = make_hard_total_recommendation(hand.get_sum_of_cards(), self.dealer_hand.get_visible_card_rank())
		print('\nThe recommended strategy is to:', strategy)

	def display_final_outcome(self, hand):
		if hand.has_blackjack():
			print('\nCongratualtions! You got Blackjack. You WIN!')
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

	# Methods used for gameplay when user splits his or her hand
	def play_split_hand(self):
		self.player_turn(self.player_hand)
		self.player_turn(self.player_second_hand)
		
		self.dealer_turn(self.player_second_hand)
		
		self.resolve_wager(self.player_hand)
		self.resolve_wager(self.player_second_hand)

	def split_hand(self):
		""" Create a second hand so the user can play using both hands
		"""
		self.player_second_hand = Hand()
		self.player_second_hand.add_card(self.player_hand.remove_last_card())  # remove card from hand 1 and give to hand 2	
		
		self.player_hand.indicate_hand_is_split()
		self.player_second_hand.indicate_hand_is_split()

		# deal a card to each hand
		self.player_hand.add_card(self.deck.deal_card())
		self.player_second_hand.add_card(self.deck.deal_card())

		# double wager
		self.winnings -= self.player_hand.wager
		self.player_second_hand.wager += self.player_hand.wager


	def display_empty_game(self):
		clear_window()
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

	def display_state_of_game(self, dealer_hand, hand):
		clear_window()
		dealer_hand.display_hand()
		hand.display_hand()
		print('\n   Funds: ${} | Bet: ${}'.format(self.winnings, hand.wager))  # display wager	


