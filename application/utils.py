from os import system, name

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