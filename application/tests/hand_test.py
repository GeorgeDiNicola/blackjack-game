import unittest, sys, os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')
from Classes.hand import *
from Classes.card import *

class Hand_Tests(unittest.TestCase):

	def test_add_card(self):
		hand = Hand()
		card = Card('S', 10)
		hand.add_card(card)
		self.assertEqual(hand.sum_of_cards, 10)
		self.assertEqual(hand.ace_count, 0)

		hand = Hand()
		card = Card('H', 'A')
		hand.add_card(card)
		self.assertEqual(hand.sum_of_cards, 11)
		self.assertEqual(hand.ace_count, 1)

	def test_has_blackjack(self):
		hand = Hand()
		card1 = Card('S', 'J')
		card2 = Card('H', 'A')
		hand.add_card(card1) 
		hand.add_card(card2)
		self.assertTrue(hand.has_blackjack())

	def test_get_over_21_status(self):
		# not over 21
		hand = Hand()
		card1 = Card('S', 10)
		card2 = Card('H', 5)
		hand.add_card(card1)
		hand.add_card(card2)
		self.assertFalse(hand.get_over_21_status())

		# over 21
		hand = Hand()
		card1 = Card('S', 10)
		card2 = Card('H', 5)
		card3 = Card('H', 7)
		hand.add_card(card1)
		hand.add_card(card2)
		hand.add_card(card3)
		self.assertTrue(hand.get_over_21_status())


if __name__ == '__main__':
	unittest.main()