import unittest, sys, os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')
from utils import *
from Classes.card import *

class utils_Tests(unittest.TestCase):

	def test_card_rank_equal(self):
		# card ranks equal
		card1 = Card('S', 10)
		card2 = Card('H', 10)
		self.assertTrue(card_rank_equal(card1, card2))

		# card ranks not equal
		card1 = Card('S', 'A')
		card2 = Card('H', 10)
		self.assertFalse(card_rank_equal(card1, card2))

	def test_get_valid_input(self):
		prompt = 'Type in the letter y: '
		possible_input = ['y']
		error_message = 'incorrect input'
		self.assertEqual(get_valid_input(prompt, possible_input, error_message), 'y')

if __name__ == '__main__':
	unittest.main()