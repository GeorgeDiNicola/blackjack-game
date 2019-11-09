import os

class Wager:

	def __init__(self):
		self.value_owned = 100
		self.allowable_bets = ['1', '5', '10', '15', '20']  #TODO change this to (1), (2), etc
		self.outstanding_bet = 0

	# mutators
	def make_wager(self):
		wager_choice = self._get_valid_wager()
		self.value_owned -= wager_choice
		self.outstanding_bet += wager_choice 

	def collect_winnings(self, blackjack=False):
		""" Add amount one back to value_owned and reset the outstanding bet
			Getting a blackjack pays 3:1
		"""
		if blackjack:
			self.value_owned += (self.outstanding_bet * 3)
		else:
			self.value_owned += (self.outstanding_bet * 2)
			self.outstanding_bet = 0

	def lose_wager(self):
		self.outstanding_bet = 0

	def return_wager_to_player(self):
	# In the case of a tie/push
		self.value_owned += self.outstanding_bet
		self.outstanding_bet = 0

	def double_wager(self):
		self.value_owned -= self.outstanding_bet
		self.outstanding_bet = self.outstanding_bet * 2

	# accessors
	def get_current_value_owned(self):
		return self.value_owned

	def get_current_wager(self):
		return self.outstanding_bet

	def _get_valid_wager(self):
		valid = False
		while not valid:
			wager_choice = input("\nHow much would you like to wager?\n  $(1)  $(5)  $(10)  $(15)  $(20)\n")
			if wager_choice in self.allowable_bets:
				if self.value_owned - int(wager_choice) < 0:
					print('You do not have enough money. Please make a lower wager.')
				else:
					valid = True
			else:
				print('Please chood a valid bet amount. Type in without the dollar sign!')
		return int(wager_choice)  #TODO might not be the best method

	def display_wager(self):
		print('\n   Funds: ${} | Bet: ${}'.format(self.value_owned, self.outstanding_bet))
