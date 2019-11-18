from os import system, name

def get_valid_input(prompt, possible_input, error_message):
	"""Retrieve valid input from the user. Repeat the prompt if the user gives invalid input.

	Keyword Arguments:
		prompt (string) -- the question/input prompt for the user.
		possible_input (list) -- the allowable input for the prompt.
		error_message (string) -- the message to output to the user when his or her input is not in the list allowable inputs.
	"""
	valid = False
	while not valid:
		choice = input(prompt)
		if choice.lower() in possible_input:
			valid = True
		else:
			print(error_message)
	return choice.lower()

def clear_window():
	"""Clear all output in the console window."""
	# for windows
	if name == 'nt':
		_ = system('cls')
	# for mac and linux
	else: 
		_ = system('clear')