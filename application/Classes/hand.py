
class Hand:

	# Constructor
	def __init__(self, isDealer = False):
		self.cards = []
		self.sum_of_cards = 0
		self.ace_count = 0
		self.isDealer = isDealer
		self.is_card_sum_over_21 = False
		self.blackjack = False

	# Mutators
	def add_card(self, card):
		self.cards.append(card)
		self._update_ace_count(card)
		self._update_sum_of_cards(card)
		self._adjust_sum_for_aces()
		self._update_over_21_status()
		if len(self.cards) == 2:  # blackjack is only possible with 2 cards in hand
			self._detect_blackjack()

	def remove_top_card(self):
		try:
			return self.cards.pop(0)
		except:
			print('There are not any cards in the hand.')

	def _update_sum_of_cards(self, card):
		self.sum_of_cards += card.value

	def _update_ace_count(self, card):
		if card.rank == 'A':
			self.ace_count += 1

	def _adjust_sum_for_aces(self):
		while self.sum_of_cards > 21 and self.ace_count > 0:
			self.sum_of_cards -= 10  # make the ace a 1
			self.ace_count -= 1  # remove used aces

	def _update_over_21_status(self):
		if self.sum_of_cards > 21:
			self.is_card_sum_over_21 = True

	def _detect_blackjack(self):
		if (self.cards[0].value == 10 and self.cards[1].rank == 'A'):
			self.blackjack = True
		elif (self.cards[1].value == 10 and self.cards[0].rank == 'A'):
			self.blackjack = True

	# Accessors
	def get_card_in_deck(self, location):
		try:
			card = self.cards[location]
		except:
			print('There are not any cards in that location of the deck')
		else:
			return card

	def get_sum_of_cards(self):
		return self.sum_of_cards

	def get_visible_cards_sum(self):
		visible_cards_sum = 0
		for card in self.cards:
			if not card.hidden:
				visible_cards_sum += card.value
		return visible_cards_sum

	def get_visible_card_rank(self):
		return self.cards[1].rank  # alter to only be dealer

	def get_over_21_status(self):
		return self.is_card_sum_over_21

	def get_blackjack_status(self):
		return self.blackjack

	def display_hand(self):
		lines = self.get_formatted_hand()
		for line in lines:
			print(line)

	def get_formatted_hand(self):
		lines = [''] * 10

		for card in self.cards:
		    if card.hidden:
		        new = card.get_formatted_face_down_card()
		        lines = [i + j for i, j in zip(lines, new)]
		    else:
		        new = card.get_formatted_face_up_card()
		        lines = [i + j for i, j in zip(lines, new)]
		    
		#lines[4] += ' <----- ' + player
		if self.cards[0].hidden:
		    lines[9] += '    Sum of cards: -'
		else:
		    lines[9] += '    Sum of cards: ' + str(self.sum_of_cards)

		formatted_hand = lines
		return formatted_hand

	def display_empty_hand(self):
		lines = [''] * 9
		for i in range(2):  # display 2 cards
		    lines[0] += '┌─────────┐' + ''
		    lines[1] += '│         │' + ''
		    lines[2] += '│         │' + ''
		    lines[3] += '│         │' + ''
		    lines[4] += '│         │' + ''
		    lines[5] += '│         │' + ''
		    lines[6] += '│         │' + '' 
		    lines[7] += '│         │' + ''
		    lines[8] += '└─────────┘' + ''
		for line in lines:
			print(line)