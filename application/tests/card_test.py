import unittest, sys, os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')
from Classes.card import *

class Card_Tests(unittest.TestCase):

	def setUp(self):
		self.card1 = Card('S', 10)
		self.card2 = Card('C', 9,)
		self.card3 = Card('H', 'A')

	def test_get_digits_in_rank(self):
		self.assertEqual(self.card1.get_digits_in_rank(), [1, 0])
		self.assertEqual(self.card2.get_digits_in_rank(), [9, ' '])
		self.assertEqual(self.card3.get_digits_in_rank(), ['A', ' '])

if __name__ == '__main__':
	unittest.main()


#assertEqual
#assertTrue
#assertFalse
# assertRaises()
#assertNotEqual
#