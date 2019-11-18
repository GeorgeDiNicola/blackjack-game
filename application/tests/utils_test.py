import unittest, sys, os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../')
from utils import *

class utils_Tests(unittest.TestCase):

	def test_get_valid_input(self):
		prompt = 'Type in the letter y: '
		possible_input = ['y']
		error_message = 'incorrect input'
		self.assertEqual(get_valid_input(prompt, possible_input, error_message), 'y')

if __name__ == '__main__':
	unittest.main()