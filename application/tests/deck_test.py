import unittest, sys, os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')
from Classes.deck import *

class Deck_Tests(unittest.TestCase):

	def setUp(self):
		self.deck = Deck()

	def test_length_of_deck(self):
		self.assertEqual(len(self.deck.cards), 52)

	def test_shuffle(self):
		self.assertNotEqual(self.deck.shuffle(), self.deck)

if __name__ == '__main__':
	unittest.main()