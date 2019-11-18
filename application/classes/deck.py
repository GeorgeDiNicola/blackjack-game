import random
from classes.card import Card

suits = ['C', 'S', 'H', 'D']

face_cards = ['J', 'Q', 'K', 'A']

class Deck:
	"""This is a class for performing operations on a deck of cards. 

	Attributes: 
        cards (list) -- the list that holds the card objects.
	"""
	def __init__(self):
		"""
		The constructor for the Deck class. It iterates through the enumerated card ranks and suits, creating a card object for each.
		"""
		deck = []
		for suit in suits:
			for rank in range(2, 11):
				StandardCard = Card(suit, rank)
				deck.append(StandardCard)
			for value in face_cards:
				FaceCard = Card(suit, value)
				deck.append(FaceCard)
		self.cards = deck

	def shuffle(self):
		"""Randomly reaarange the cards inside of the deck."""
		random.shuffle(self.cards)

	def deal_card(self):
		"""Remove the card object at the top of the deck and return it."""
		try:
			return self.cards.pop(0)
		except:
			print('There are no cards left in the deck.')