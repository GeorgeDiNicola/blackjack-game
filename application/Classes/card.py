value_lookup = {
		'J': 10,
		'Q': 10,
		'K': 10,
		'A': 11  # assume Aces eleven unless users forces them to be a 1 during gameplay
} 
suit_icons = {
                'S': '♠',
                'D': '♦',
                'H': '♥',
                'C': '♣'
}

max_card_height = 10

class Card:

	def __init__(self, suit, rank, facedown=False):
		self.suit = suit
		self.rank = rank
		if not isinstance(self.rank, int):
			self.value = value_lookup[self.rank]
		else:
			self.value = self.rank
		self.facedown = facedown

	def flip_face_up(self):
		self.facedown = False

	def flip_face_down(self):
		self.facedown = True

	def get_rank_digit_list(self):
		if isinstance(self.rank, int) and self.rank == 10:
			return [1, 0]
		else:
			return [self.rank, ' ']

	def get_formatted_face_up_card(self):
		lines = [''] * max_card_height
		rank_digit_list = self.get_rank_digit_list()
		lines[0] += '┌─────────┐'
		lines[1] += '│{}{}       │'.format(rank_digit_list[0], rank_digit_list[1])
		lines[2] += '│         │' 
		lines[3] += '│         │'
		lines[4] += '│    {}    │'.format(suit_icons[self.suit])
		lines[5] += '│         │'
		lines[6] += '│         │'
		lines[7] += '│       {}{}│'.format(rank_digit_list[0], rank_digit_list[1])
		lines[8] += '└─────────┘'
		return lines

	def get_formatted_face_down_card(self):
		lines = [''] * max_card_height
		lines[0] += '┌─────────┐'
		lines[1] += '│░░░░░░░░░│'
		lines[2] += '│░░░░░░░░░│'
		lines[3] += '│░░░░░░░░░│'
		lines[4] += '│░░░░░░░░░│'
		lines[5] += '│░░░░░░░░░│'
		lines[6] += '│░░░░░░░░░│'
		lines[7] += '│░░░░░░░░░│'
		lines[8] += '└─────────┘'
		return lines