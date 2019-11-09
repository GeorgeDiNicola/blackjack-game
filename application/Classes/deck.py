import random

from Classes.card import Card

suits = ['C', 'S', 'H', 'D']

face_cards = ['J', 'Q', 'K', 'A']

class Deck:

	def __init__(self):
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
		random.shuffle(self.cards)

	def deal_card(self):
		try:
			return self.cards.pop(0)
		except:
			print('There are no cards left in the deck.')