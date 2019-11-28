import unittest, sys, os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')
from blackjack_strategy import *

class blackjack_strategy_Tests(unittest.TestCase):

	def test_make_pair_recommendation(self):
		self.assertEqual(make_pair_recommendation(8, 10), 'Split')
		self.assertEqual(make_pair_recommendation(2, 8), 'Hit')
		self.assertEqual(make_pair_recommendation('J', 'Q'), 'Stand')

	def test_make_hard_total_recommendation(self):
		self.assertEqual(make_hard_total_recommendation(9, 2), 'Hit')
		self.assertEqual(make_hard_total_recommendation(9, 5), 'Double Down (Hit)')
		self.assertEqual(make_hard_total_recommendation(12, 4), 'Stand')

	def test_make_soft_total_recommendation(self):
		self.assertEqual(make_soft_total_recommendation(2, 'A'), 'Hit')
		self.assertEqual(make_soft_total_recommendation(4, 4), 'Double Down (Hit)')
		self.assertEqual(make_soft_total_recommendation(8, 'Q'), 'Stand')

if __name__ == '__main__':
	unittest.main()