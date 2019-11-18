import unittest, sys, os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')
from Classes.card import *

class Card_Tests(unittest.TestCase):

	def setUp(self):
		self.card1 = Card('S', 'K')
		self.card2 = Card('S', 10)
		self.card3 = Card('C', 9,)
		self.card4 = Card('H', 'A')

	def test_card_value_lookup(self):
		self.assertEqual(self.card1.value, 10)

	def test_get_rank_digit_list(self):
		self.assertEqual(self.card2.get_rank_digit_list(), [1, 0])
		self.assertEqual(self.card3.get_rank_digit_list(), [9, ' '])
		self.assertEqual(self.card4.get_rank_digit_list(), ['A', ' '])

if __name__ == '__main__':
	unittest.main()