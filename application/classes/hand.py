import utils as util

first_card = 0
second_card = 1
max_card_height = 10

class Hand:

	def __init__(self, isDealer = False):
		self.isDealer = isDealer
		self.cards = []
		self.sum_of_cards = 0
		self.ace_count = 0
		self.is_split = False
		self.wager = 0

	def add_card(self, card):
		self.cards.append(card)
		self._update_ace_count(card)
		self._update_sum_of_cards(card)
		self._adjust_sum_for_aces()

	def _update_ace_count(self, card):
		if card.rank == 'A':
			self.ace_count += 1
	
	def _update_sum_of_cards(self, card):
		self.sum_of_cards += card.value

	def _adjust_sum_for_aces(self):
		while self.sum_of_cards > 21 and self.ace_count > 0:
			self.sum_of_cards -= 10  # make the ace a 1
			self.ace_count -= 1  # remove used aces

	def remove_last_card(self):
		try:
			card = self.cards.pop()
		except:
			print('There are not any cards in the hand.')
		else:
			self.sum_of_cards -= card.value
			return card

	def indicate_hand_is_split(self):
		self.is_split = True

	def reset_wager(self):
		self.wager = 0

	def prompt_for_wager(self, winnings):
		prompt = "\nHow much would you like to wager?\n  $(1)  $(5)  $(10)  $(15)  $(20)\n\nWager Amount: "
		allowable_bets = ['1', '5', '10', '15', '20']
		error_message = 'Please choose a valid bet amount. Type in without the dollar sign!'
		input_invalid = True
		while input_invalid:
			wager_choice = util.get_valid_input(prompt, allowable_bets, error_message)
			if winnings - int(wager_choice) < 0:
				print('You do not have enough money. Please make a lower wager.')
			else:
				input_invalid = False
		self.wager = int(wager_choice)

	def has_blackjack(self):
		if (self.cards[first_card].value == 10 and self.cards[second_card].rank == 'A'):
			return True
		elif (self.cards[second_card].value == 10 and self.cards[first_card].rank == 'A'):
			return True
		else:
			return False

	def get_over_21_status(self):
		if self.sum_of_cards > 21:
			return True
		else:
			return False

	def display_hand(self):
		lines = self._format_hand()
		for line in lines:
			print(line)

	def _format_hand(self):
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