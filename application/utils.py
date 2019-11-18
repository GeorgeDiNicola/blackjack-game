from os import system, name 
from strategyTables import hard_totals, soft_totals, pair_splitting

def get_valid_input(prompt, possible_input, error_message):
	valid = False
	while not valid:
		choice = input(prompt)
		if choice.lower() in possible_input:
			valid = True
		else:
			print(error_message)
	return choice.lower()

def clear_window():
    # for windows 
    if name == 'nt': 
        _ = system('cls')
    # for mac and linux
    else: 
        _ = system('clear')

def make_pair_recommendation(rank, sum_of_dealer_hand):
	strategy = pair_splitting.get((rank, sum_of_dealer_hand))
	if strategy == None:
		strategy = 'Stand'
	return strategy

def make_hard_total_recommendation(sum_of_cards, sum_of_dealer_hand):
	strategy = hard_totals.get((sum_of_cards, sum_of_dealer_hand))
	if strategy == None and sum_of_cards < 8:
		strategy = 'Hit'
	elif strategy == None and sum_of_cards > 17:
		strategy = 'Stand'
	return strategy

def make_soft_total_recommendation(rank, sum_of_dealer_hand):
	strategy = soft_totals.get((rank, sum_of_dealer_hand))
	return strategy