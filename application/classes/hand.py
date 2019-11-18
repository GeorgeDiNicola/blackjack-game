import utils as util

first_card = 0
second_card = 1
max_card_height = 10

class Hand:
	"""This is a class for performing operations on and retrieving information about the Card . 

	Attributes: 
        isDealer (bool) -- an indication of whether the hand belongs to the dealer (false indicates it belongs to the player).
        cards (list) -- contains each of the card objects in the hand.
        sum_of_cards (int) -- the total value of all of the cards in the hand.
        ace_count (int) -- the number of aces in the hand.
        is_split (bool) -- an indication of whether the hand has been split during the game.
        wager (int) -- the value the player has wagered on the hand.
	"""
	def __init__(self, isDealer = False):
		"""The constructor for the Hand class.

		Keyword arguments:
			isDealer (bool) -- an indication of whether the hand belongs to the dealer (default False).
        	cards (list) -- contains each of the card objects in the hand.
        	sum_of_cards (int) -- the total value of all of the cards in the hand.
        	ace_count (int) -- the number of aces in the hand.
        	is_split (bool) -- an indication of whether the hand has been split during the game.
		"""
		self.isDealer = isDealer
		self.cards = []
		self.sum_of_cards = 0
		self.ace_count = 0
		self.is_split = False
		self.wager = 0

	def add_card(self, card):
		"""Add a card to the hand. Update the ace_count and sum_of_cards attributes. Adjust sum based on the aces and total.

		Keyword arguments:
			card (Card) -- the card object to be added to the had.
		"""
		self.cards.append(card)
		self._update_ace_count(card)
		self._update_sum_of_cards(card)
		self._adjust_sum_for_aces()

	def _update_ace_count(self, card):
		"""Add 1 to the ace count of the hand if an ace is added the the hand."""
		if card.rank == 'A':
			self.ace_count += 1
	
	def _update_sum_of_cards(self, card):
		"""Add the value of the card to the current sum of cards of the hand."""
		self.sum_of_cards += card.value

	def _adjust_sum_for_aces(self):
		"""When a new card is added the the hand and it causes the sum of the cards in the hand to be more than 21, 
			change the value of the aces to 1 until the sum is below 21.
		"""
		while self.sum_of_cards > 21 and self.ace_count > 0:
			self.sum_of_cards -= 10  # make the ace a 1
			self.ace_count -= 1  # remove used aces

	def remove_last_card(self):
		"""Remove the last card in the hand and return it. Subtract its value from the sum of the cards."""
		try:
			card = self.cards.pop()
		except:
			print('There are not any cards in the hand.')
		else:
			self.sum_of_cards -= card.value
			return card

	def indicate_hand_is_split(self):
		"""Set the hand as split."""
		self.is_split = True

	def reset_wager(self):
		"""Set the wager to zero."""
		self.wager = 0

	def prompt_for_wager(self, winnings):
		"""Ask the player to wager an amount from their winnings on the hand.

		Keyword Arguments:
			winnings (int) -- The amount of money the player has. 
		"""
		prompt = "\nHow much would you like to wager?\n  $(1)  $(5)  $(10)  $(15)  $(20)\n\nWager Amount: "
		allowable_bets = ['1', '5', '10', '15', '20']
		error_message = 'Please choose a valid bet amount. Type in without the dollar sign!'
		input_invalid = True
		while input_invalid:
			wager_choice = util.get_valid_input(prompt, allowable_bets, error_message)
			if winnings - int(wager_choice) < 0:  # ensure the player has enough money to make the wager he or she chooses.
				print('You do not have enough money. Please make a lower wager.')
			else:
				input_invalid = False
		self.wager = int(wager_choice)

	def has_blackjack(self):
		"""Determine if the hand has blackjack (Ace and a card with the value of 10)."""
		if (self.cards[first_card].value == 10 and self.cards[second_card].rank == 'A'):
			return True
		elif (self.cards[second_card].value == 10 and self.cards[first_card].rank == 'A'):
			return True
		else:
			return False

	def get_over_21_status(self):
		"""Return whether the hand's sum is greater than 21."""
		if self.sum_of_cards > 21:
			return True
		else:
			return False

	def display_hand(self):
		"""Display the hand to the console, printing it line by line."""
		lines = self._format_hand()
		for line in lines:
			print(line)

	def _format_hand(self):
		"""Format a user interface that will display the hand to the player and indicate the owner of the hand (Dealer or Player)."""
		lines = [''] * max_card_height
		for card in self.cards:
		    if card.facedown:
		        new = card.get_formatted_face_down_card()
		        lines = [i + j for i, j in zip(lines, new)]  # append lists item-wise
		    else:
		        new = card.get_formatted_face_up_card()
		        lines = [i + j for i, j in zip(lines, new)]  # append lists item-wise
		
		if self.isDealer:
			lines[4] += ' <----- Dealer'
		else:
			lines[4] += ' <----- Player'
		
		if self.cards[first_card].facedown:
		    lines[9] += '    Sum of cards: -'
		else:
		    lines[9] += '    Sum of cards: ' + str(self.sum_of_cards)
		return lines